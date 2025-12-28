import os
from typing import Callable, Dict, Optional

import yt_dlp


def download_video(
    url: str,
    output_template: str,
    custom_options: Optional[Dict] = None,
    progress_callback: Optional[Callable[[Dict], None]] = None,
) -> str:
    """Download remote video content to disk and return the resulting filename."""
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    if custom_options:
        ydl_opts.update(custom_options)

    if progress_callback:
        ydl_opts["progress_hooks"] = [progress_callback]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
        if not filename.lower().endswith(".mp4"):
            filename = os.path.splitext(filename)[0] + ".mp4"

    if not os.path.exists(filename):
        raise FileNotFoundError("Failed to download video.")

    return filename
