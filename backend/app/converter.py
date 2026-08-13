import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from app.config import CONVERSION_MATRIX, CONVERSION_TIMEOUT_SECONDS, SOFFICE


def _run_external(cmd: list[str], timeout: int = CONVERSION_TIMEOUT_SECONDS) -> None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"La conversión tardó más de lo esperado: {timeout} segundos.")
    if result.returncode != 0:
        raise RuntimeError(f"El proceso de conversión falló: {result.stderr.strip()}")


def convert_with_libreoffice(source_path: Path, out_dir: Path, target_format: str) -> Path:
    """Convierte con LibreOffice headless a cualquier formato de --convert-to."""
    if not Path(SOFFICE).exists():
        raise RuntimeError(f"No se encontró LibreOffice en: {SOFFICE}")

    # Perfil aislado y único por conversión (evita candados entre procesos simultáneos).
    # El "with" mantiene viva la carpeta DURANTE la conversión y la borra al final.
    with tempfile.TemporaryDirectory(prefix="lo_profile_") as profile_dir:
        cmd = [
            SOFFICE,
            "--headless",
            "--norestore",
            "-env:UserInstallation=" + Path(profile_dir).as_uri(),
        ]
        # Sin el infilter explícito, LibreOffice no reconoce el importador PDF
        # ("no export filter ... found, aborting") en varias versiones.
        if Path(source_path).suffix.lower() == ".pdf":
            cmd.append("--infilter=writer_pdf_import")
        cmd += [
            "--convert-to", target_format,
            "--outdir", str(out_dir),
            str(source_path),
        ]
        _run_external(cmd)

    output = out_dir / f"{source_path.stem}.{target_format}"
    if not output.exists():
        raise RuntimeError("LibreOffice terminó sin generar el archivo de salida.")
    return output


def convert_image_to_pdf(source_path: Path, out_dir: Path) -> Path:
    out = out_dir / f"{source_path.stem}.pdf"
    with Image.open(source_path) as img:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(out, "PDF", resolution=150)
    return out


def convert_image_to_format(source_path: Path, out_dir: Path, target_ext: str) -> Path:
    out = out_dir / f"{source_path.stem}.{target_ext}"
    with Image.open(source_path) as img:
        if target_ext in ("jpg", "jpeg") and img.mode not in ("RGB", "L"):
            img = img.convert("RGB")  # JPEG no admite transparencia/alpha
        # Pillow registra el formato como "JPEG", no "JPG".
        format_name = "JPEG" if target_ext in ("jpg", "jpeg") else target_ext.upper()
        img.save(out, format=format_name)
    return out


def convert_file(source_path: Path, out_dir: Path, input_ext: str, target_ext: str) -> Path:
    """Resuelve el motor según la matriz y ejecuta la conversión."""
    engine = CONVERSION_MATRIX.get(input_ext, {}).get(target_ext)
    if engine is None:
        raise RuntimeError(f"No se soporta convertir de {input_ext} a .{target_ext}")
    if engine == "libreoffice":
        return convert_with_libreoffice(source_path, out_dir, target_ext)
    if engine == "pillow":
        if target_ext == "pdf":
            return convert_image_to_pdf(source_path, out_dir)
        return convert_image_to_format(source_path, out_dir, target_ext)
    raise RuntimeError(f"Motor no disponible: {engine}")