from pathlib import Path
import os
import shutil

# SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

SOFFICE = (
    os.environ.get("SOFFICE_PATH")
    or shutil.which("soffice")
    or r"C:\Program Files\LibreOffice\program\soffice.exe"
)

ALLOWED_EXTENSIONS = {".docx", ".xlsx", ".pptx"}

MAX_UPLOAD_BYTES = 25 * 1024 * 1024 # 25 MB

CONVERSION_TIMEOUT_SECONDS = 120