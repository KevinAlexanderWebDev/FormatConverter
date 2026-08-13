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

MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB

CONVERSION_TIMEOUT_SECONDS = 120

# Estos son los formatos de entrada (claves de matriz).
# Multimedia (FFmpeg) queda fuera de alcance por ahora.
INPUT_EXTENSIONS = {
    ".docx", ".xlsx", ".pptx", ".pdf",
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif",
}

# Matriz de conversión: extensión de entrada -> { formato destino: motor }
CONVERSION_MATRIX = {
    ".docx": {"pdf": "libreoffice"},
    ".xlsx": {"pdf": "libreoffice"},
    ".pptx": {"pdf": "libreoffice"},
    ".pdf": {"docx": "libreoffice", "xlsx": "libreoffice", "pptx": "libreoffice"},
    ".png": {"pdf": "pillow", "jpg": "pillow", "webp": "pillow", "gif": "pillow", "bmp": "pillow", "tiff": "pillow"},
    ".jpg": {"pdf": "pillow", "png": "pillow", "webp": "pillow", "gif": "pillow", "bmp": "pillow", "tiff": "pillow"},
    ".jpeg": {"pdf": "pillow", "png": "pillow", "webp": "pillow", "gif": "pillow", "bmp": "pillow", "tiff": "pillow"},
    ".webp": {"pdf": "pillow", "png": "pillow", "jpg": "pillow", "gif": "pillow", "bmp": "pillow"},
    ".gif": {"pdf": "pillow", "png": "pillow", "jpg": "pillow", "webp": "pillow", "bmp": "pillow"},
    ".bmp": {"pdf": "pillow", "png": "pillow", "jpg": "pillow", "webp": "pillow", "gif": "pillow"},
    ".tiff": {"pdf": "pillow", "png": "pillow", "jpg": "pillow", "webp": "pillow"},
    ".tif": {"pdf": "pillow", "png": "pillow", "jpg": "pillow", "webp": "pillow"},
}

MIME_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
}