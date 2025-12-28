import asyncio

from fastapi import APIRouter

from app.downloaders.youtube import YOUTUBE_DOWNLOADER
from app.services.download_tracker import DOWNLOAD_TRACKER

router = APIRouter(prefix="/youtube", tags=["YouTube"])


@router.post("/download")
async def request_youtube_download(url: str):
    """Kick off a YouTube download and return a process identifier."""
    job = DOWNLOAD_TRACKER.create_job(source="youtube", url=url)

    async def runner():
        try:
            await YOUTUBE_DOWNLOADER.download(url, job.process_id)
        except Exception as exc:
            DOWNLOAD_TRACKER.update_job(
                job.process_id, status="failed", error=str(exc)
            )

    asyncio.create_task(runner())
    return {"process_id": job.process_id}
