import subprocess
import tempfile
from pathlib import Path

from app.config import CONVERSION_TIMEOUT_SECONDS, SOFFICE


def convert_office_to_pdf(source_path: Path, out_dir: Path) -> Path:
    """Convierte un archivo de Office a PDF usando LibreOffice headless."""
    if not Path(SOFFICE).exists():
        raise RuntimeError(f"No se encontró LibreOffice en: {SOFFICE}")

    # Perfil aislado y único por conversión: LibreOffice usa una carpeta de usuario
    # con candados, y dos procesos simultáneos chocarían por el mismo perfil.
    # El "with" mantiene viva la carpeta DURANTE la conversión y la borra al final.
    with tempfile.TemporaryDirectory(prefix="lo_profile_") as profile_dir:
        user_install = Path(profile_dir).as_uri()

        # Los argumentos de la línea de comandos van en una lista (sin concatenar strings)
        cmd = [
            SOFFICE,
            "--headless",       # sin interfaz gráfica (modo servidor)
            "--norestore",      # no restaurar sesiones anteriores
            "-env:UserInstallation=" + user_install,
            "--convert-to", "pdf",
            "--outdir", str(out_dir),
            str(source_path),
        ]

        try:
            # Ejecuta el proceso externo y espera a que termine
            result = subprocess.run(
                cmd,
                capture_output=True,  # captura stdout y stderr en vez de imprimir
                text=True,            # devuelve salida como texto, no bytes
                timeout=CONVERSION_TIMEOUT_SECONDS,
                check=False,          # no lanzar excepción solo por returncode != 0
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f"La conversión tardó más de {CONVERSION_TIMEOUT_SECONDS} segundos."
            )

    # LibreOffice nombra el PDF con el mismo nombre base del archivo origen
    pdf_path = out_dir / (source_path.stem + ".pdf")

    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"LibreOffice falló: {result.stderr.strip()}")

    return pdf_path
