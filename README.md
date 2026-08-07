# Format-Converter

Convierte archivos de Office (Word, Excel, PowerPoint) a PDF.

## Stack
- Frontend: Blazor WebAssembly (C# / .NET 9)
- Backend: FastAPI (Python) + LibreOffice headless

## Estructura
- `backend/` — API REST de conversión
- `frontend/` — SPA en Blazor WebAssembly

## Fase actual
Backend vivo con endpoint /health (Fase 1).
0.4 Primer commit (PowerShell)
git add .
git commit -m "Fase 0: cimientos del monorepo"
Verifica el resultado: git status debe mostrar nada pendiente, y git log --oneline debe mostrar tu primer commit.