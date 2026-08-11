import shutil
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_BYTES
from app.converter import convert_office_to_pdf

#CORS: Permite que otro navegador cuyo puerto es distinto pueda llamar a la API por su puerto y el navegador lo bloquee
# Instancia de la app: registramos todas las rutas
app = FastAPI(title="Format Converter Api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5291"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Zona Endpoints (el decorador @app.get asocia la funcion de abajo a GET /health)
@app.get("/health")
def health():
    # FastApi convierte auth este dict a JSON
    return {"status":"ok"}
@app.post("/convert")
def convert(file: UploadFile = File(...)):
    # 1) Validamos la extensión ANTES de escribir nada en disco.
    #    file.filename lo controla el cliente: no confiamos en él.
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS: 
        raise HTTPException(status_code=415, 
                            detail=f"Formato no soportado. Usa: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
                            )
    # 2) Carpeta temporal privada para esta conversión.
    #    El "with" garantiza que se borre sola al terminar (éxito o error).
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
    # 3) Guardamos el archivo con un nombre FIJO "input{ext}".
    #    Evitamos inyecciones de rutas (../../etc/passwd) del nombre del cliente.
        source_path = tmp_dir / f"input{ext}"
        size = 0 # Realizamos copia de 1 MB por bloques contando bytes, si se superan abortamos inst. con un 413 status code
        with source_path.open("wb") as buffer:
            while chunk := file.file.read(1024 * 1024): 
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="El archivo supera el límite de 25 MB.",)
                buffer.write(chunk)
     # 4) Conversión. Los errores internos se traducen a HTTP 500 con mensaje claro.
        try:
            pdf_path = convert_office_to_pdf(source_path, tmp_dir)
        except RuntimeError as error:
            raise HTTPException(status_code=500, detail=str(error))
        # 5) Leemos el PDF en memoria DENTRO del "with".
            #    El TemporaryDirectory se borra al salir del bloque, pero la respuesta
            #    HTTP se envía DESPUÉS de retornar: el archivo ya no existiría.
        pdf_bytes = pdf_path.read_bytes()
     # 6) Devolvemos el PDF como archivo descargable
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition":
                f'attachment; filename="{Path(file.filename).stem}.pdf"'},
    )
    

    
    