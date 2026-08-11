def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_convert_unsupported_extension(client):
    response = client.post("/convert", files={"file": ("hola.txt", b"texto", "text/plain")})
    assert response.status_code == 415


def test_convert_without_file(client):
    response = client.post("/convert")
    assert response.status_code == 422


def test_convert_docx_to_pdf(client, sample_docx):
    with sample_docx.open("rb") as f:
        response = client.post(
            "/convert",
            files={"file": ("sample.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    # "%PDF" son los 4 bytes con los que SIEMPRE empieza un PDF válido (firma mágica)
    assert response.content[:4] == b"%PDF"


def test_convert_too_large(client):
    big = b"x" * (26 * 1024 * 1024)  # 26 MB: supera el límite
    response = client.post("/convert", files={"file": ("grande.docx", big, "application/octet-stream")})
    assert response.status_code == 413