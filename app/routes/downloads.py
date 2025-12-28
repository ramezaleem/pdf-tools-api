import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.download_tracker import DOWNLOAD_TRACKER
from app.utils.file_ops import ascii_filename

router = APIRouter(prefix="/downloads", tags=["Download Jobs"])


@router.get("/{process_id}")
async def get_download_status(process_id: str):
    payload = DOWNLOAD_TRACKER.serialize_job(process_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Process not found")
    return payload


@router.get("/{process_id}/file")
async def get_downloaded_file(process_id: str):
    job = DOWNLOAD_TRACKER.get_job(process_id)
    if not job:
        raise HTTPException(status_code=404, detail="Process not found")
    if job.status != "completed" or not job.file_path or not os.path.exists(job.file_path):
        raise HTTPException(status_code=400, detail="File not ready")

    safe_filename = ascii_filename(job.suggested_name or os.path.basename(job.file_path))
    return FileResponse(job.file_path, filename=safe_filename)
