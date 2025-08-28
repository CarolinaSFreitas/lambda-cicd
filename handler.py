import os, json, base64, mimetypes
from pathlib import Path

# pasta do código (mesmo nível dos arquivos)
BASE = Path(__file__).parent

def _resp(status=200, body="", ctype="text/plain; charset=utf-8", b64=False, extra_headers=None):
    headers = {
        "Content-Type": ctype,
        "Cache-Control": "no-store",         # ajuste se quiser cache
    }
    if extra_headers:
        headers.update(extra_headers)
    return {
        "statusCode": status,
        "headers": headers,
        "isBase64Encoded": b64,
        "body": body if not b64 else base64.b64encode(body).decode("ascii"),
    }

def handler(event, context):
    # Function URL usa HTTP payload (rawPath, method, etc)
    path = (event.get("rawPath") or "/").rstrip("/") or "/"
    if path == "/":
        path = "/index.html"

    # mapeia caminho -> arquivo local
    local = BASE / path.lstrip("/")
    if not local.exists() or not local.is_file():
        return _resp(404, "Not found")

    # content-type
    ctype, _ = mimetypes.guess_type(str(local))
    if not ctype:
        ctype = "application/octet-stream"

    # arquivos de texto vs binários (imagens etc.)
    # Para imagens/binários, devolvemos como base64.
    binary_types = ("image/", "font/", "application/octet-stream")
    data = local.read_bytes()
    is_binary = ctype.startswith(binary_types)

    # CORS opcional (se quiser abrir para outros domínios)
    extra = {
        # "Access-Control-Allow-Origin": "*"
    }

    return _resp(200, data if is_binary else data.decode("utf-8"), ctype, b64=is_binary, extra_headers=extra)
