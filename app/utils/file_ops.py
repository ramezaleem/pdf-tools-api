import os
import re
import threading
import time
import unicodedata
import uuid

from fastapi import UploadFile

from app.config import CHUNK_SIZE


def ascii_filename(filename: str) -> str:
    """Sanitize filename for HTTP headers (ASCII only)."""
    nfkd = unicodedata.normalize("NFKD", filename)
    only_ascii = nfkd.encode("ASCII", "ignore").decode("ASCII")
    return re.sub(r"[^A-Za-z0-9._-]", "_", only_ascii)


def delete_file_later(file_path: str, delay: int = 300) -> None:
    """Delete a file after a delay (default 5 minutes)."""

    def delete():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)

    threading.Thread(target=delete, daemon=True).start()


def safe_stem(filename: str) -> str:
    """Return a sanitized stem for derived files."""
    stem = os.path.splitext(os.path.basename(filename))[0]
    sanitized = ascii_filename(stem)
    return sanitized or "file"


async def save_upload_file(upload_file: UploadFile, destination_folder: str) -> str:
    """Persist UploadFile contents to disk using chunks to avoid large memory spikes."""
    ext = os.path.splitext(upload_file.filename)[1]
    unique_name = uuid.uuid4().hex + (ext.lower() if ext else "")
    file_path = os.path.join(destination_folder, unique_name)

    with open(file_path, "wb") as buffer:
        while True:
            chunk = await upload_file.read(CHUNK_SIZE)
            if not chunk:
                break
            buffer.write(chunk)

    await upload_file.seek(0)
    return file_path
