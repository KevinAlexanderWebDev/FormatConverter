# Format-Converter

![CI](https://github.com/KevinAlexanderWebDev/FormatConverter/actions/workflows/ci.yaml/badge.svg)
![Deploy](https://github.com/KevinAlexanderWebDev/FormatConverter/actions/workflows/gh-pages.yaml/badge.svg)

Convierte archivos de Office (Word, Excel, PowerPoint) a PDF.

## Stack
- Frontend: Blazor WebAssembly (C# / .NET 9)
- Backend: FastAPI (Python) + LibreOffice headless

## Estructura
- `backend/` — API REST de conversión
- `frontend/` — SPA en Blazor WebAssembly

## Estado actual
Fases 1-5 completadas: API de conversión, frontend Blazor, robustez y contenedores.
Despliegue: backend en Render, frontend en GitHub Pages.

## CI/CD (Fase 7)
- `ci.yaml` — tests del backend, build del frontend y validación de JSON en cada push/PR.
- `gh-pages.yaml` — despliega el frontend en GitHub Pages cuando CI pasa.

Sitio: https://KevinAlexanderWebDev.github.io/FormatConverter/
