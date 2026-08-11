# Python 3.14 ft. Debian slim (liviana version)
FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Orden especifico 
# 1º dependencias, 2º código. Cada línea de un Dockerfile es una
# "capa". Docker reutiliza las capas que no cambiaron entre builds.
# requirements.txt cambia rara vez → su capa se cachea → builds rápidos.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# El código cambia en CADA commit → esta capa se reconstruye siempre.
COPY app ./app

# Puerto que expone la API dentro del contenedor (documental)
EXPOSE 8000

# Arranque de PRODUCCIÓN:
#  - sin --reload (aprendido en Fase 1)
#  - --host 0.0.0.0 : escucha en TODAS las interfaces del contenedor,
#    no solo localhost interno.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]