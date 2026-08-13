import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.config import CONVERSION_MATRIX, INPUT_EXTENSIONS, MAX_UPLOAD_BYTES, MIME_TYPES
from app.converter import convert_file

# CORS: permite que el navegador (otro origen) pueda llamar a la API
# sin que el navegador lo bloquee. Orígenes vía variable de entorno.
CORS_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "CORS_ORIGIN", 
        "http://localhost:5291,https://kevinalexanderwebdev.github.io",
    ).split(",")
    if o.strip()
]

app = FastAPI(title="Format Converter API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    # FastAPI convierte automáticamente este dict a JSON
    return {"status": "ok"}


@app.post("/convert")
def convert(file: UploadFile = File(...), to_format: str = Form("pdf")):
    # 1) Validamos la extensión de entrada ANTES de escribir nada en disco.
    #    file.filename lo controla el cliente: no confiamos en él.
    ext = Path(file.filename or "").suffix.lower()
    if ext not in INPUT_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Formato de entrada no soportado: {ext}",
        )

    # 2) Normalizamos y validamos el formato de salida (415 temprano).
    to_ext = to_format.lower().lstrip(".")
    if ext == f".{to_ext}":
        raise HTTPException(
            status_code=415,
            detail="El formato de entrada es igual al de salida.",
        )
    if to_ext not in CONVERSION_MATRIX.get(ext, {}):
        raise HTTPException(
            status_code=415,
            detail=f"No se soporta convertir de {ext} a .{to_ext}",
        )

    # 2) Carpeta temporal privada para esta conversión.
    #    El "with" garantiza que se borre sola al terminar (éxito o error).
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        # 3) Guardamos el archivo con un nombre FIJO "input{ext}".
        #    Evitamos inyecciones de rutas (../../etc/passwd) del nombre del cliente.
        source_path = tmp_dir / f"input{ext}"

        # Copiamos por bloques de 1 MB contando bytes:
        # si se supera el límite, abortamos al momento con un 413.
        size = 0
        with source_path.open("wb") as buffer:
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(
                        status_code=413,  # Payload Too Large
                        detail="El archivo supera el límite de 25 MB.",
                    )
                buffer.write(chunk)

        # 4) Conversión. Los errores internos se traducen a HTTP 500 con mensaje claro.
        try:
            output_path = convert_file(source_path, tmp_dir, ext, to_ext)
        except RuntimeError as error:
            raise HTTPException(status_code=500, detail=str(error))

        # 5) Leemos el archivo de salida en memoria DENTRO del "with".
        #    El TemporaryDirectory se borra al salir del bloque, pero la respuesta
        #    HTTP se envía DESPUÉS de retornar: el archivo ya no existiría.
        bytes_out = output_path.read_bytes()

    # 6) Devolvemos el archivo como descarga
    return Response(
        content=bytes_out,
        media_type=MIME_TYPES.get(to_ext, "application/octet-stream"),
        headers={"Content-Disposition":
                 f'attachment; filename="{Path(file.filename).stem}.{to_ext}"'},)