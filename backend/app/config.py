import os
import shutil

# Orden de resolución de la ruta de LibreOffice:
#  1) Variable de entorno SOFFICE_PATH (si se define)
#  2) Ruta en el PATH del sistema (Linux: "/usr/bin/soffice")
#  3) Ruta fija de Windows (tu máquina)
SOFFICE = (
    os.environ.get("SOFFICE_PATH")
    or shutil.which("soffice")
    or r"C:\Program Files\LibreOffice\program\soffice.exe"
)

ALLOWED_EXTENSIONS = {".docx", ".xlsx", ".pptx"}

MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB

CONVERSION_TIMEOUT_SECONDS = 120