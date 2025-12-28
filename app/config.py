import os

DOWNLOAD_FOLDER = "downloads"
PDF_DOWNLOAD_FOLDER = "pdf_uploads"
EXCEL_DOWNLOAD_FOLDER = "excel_outputs"
WORD_DOWNLOAD_FOLDER = "word_outputs"
IMAGE_DOWNLOAD_FOLDER = "image_outputs"

for folder in (
    DOWNLOAD_FOLDER,
    PDF_DOWNLOAD_FOLDER,
    EXCEL_DOWNLOAD_FOLDER,
    WORD_DOWNLOAD_FOLDER,
    IMAGE_DOWNLOAD_FOLDER,
):
    os.makedirs(folder, exist_ok=True)

CHUNK_SIZE = 1024 * 1024  # 1MB
YOUTUBE_REMOTE_ENDPOINT = os.environ.get("YOUTUBE_REMOTE_ENDPOINT")
