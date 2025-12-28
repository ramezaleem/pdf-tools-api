## Integrate the PDF→Image Endpoint

This app already exposes `/pdf/to-image`, so integration is mostly about wiring it into `FastAPI` and your client. Here is what you need to know:

### 1. Enable the route

The `main.py` module currently comments out the PDF router. Re-enable it by importing the router and including it:

```python
from app.routes.pdf import router as pdf_router

app.include_router(pdf_router)
```

That router wires `/pdf/to-image` (and the other PDF conversions) to `/pdf` plus the path shown above. The handler uses `asyncio.to_thread` and `create_images_zip` to keep FastAPI responsive while PyMuPDF renders each page.

### 2. Dependencies

Only the PDF→image endpoint requires `PyMuPDF` (module `fitz`) plus the standard library `zipfile`. Install it alongside the rest of the project requirements:

```bash
pip install PyMuPDF
```

The config file already creates the `image_outputs` folder, so no additional folder setup is needed.

### 3. How clients call the endpoint

- Method: `POST`
- Path: `/pdf/to-image`
- Content type: `multipart/form-data`
- Field: `file` with the PDF payload

Example `curl` call:

```bash
curl -X POST "http://localhost:8000/pdf/to-image" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf" \
  --output document-images.zip
```

The server responds with a `FileResponse` delivering a ZIP archive named after the original PDF. Headers use `Content-Disposition` so browsers treat it as an attachment.

### 4. Result handling

Inside `create_images_zip`, each PDF page is rendered as PNG and saved to a temporary session folder under `image_outputs/<safe-name>_<uuid>`. After zipping, the folder is deleted immediately and the ZIP file is cleaned up after 10 minutes via `delete_file_later`.

The archive contains files named `<original-name>_page_<n>.png`. If no pages are found, the route raises a `400`-style JSON error (the same format is used for validation, file saving, or rendering exceptions).

### 5. Customization guidelines

1. Use `app/config.py` to relocate `IMAGE_DOWNLOAD_FOLDER` if your deployment needs a different path.
2. Adjust `delete_file_later` delays or rejection responses in `app/routes/pdf.py` if you need longer availability or different cleanup behavior.
3. On the client side, unzip the response and consume the PNG files directly (they are standard RGB PNGs from PyMuPDF).

With the router re-enabled and `PyMuPDF` installed, the endpoint is ready to accept uploads and return the generated images in a ZIP archive.
