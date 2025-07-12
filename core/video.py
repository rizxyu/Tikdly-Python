from urllib.parse import urlparse
import os
import requests
import json
from rich.console import Console

console = Console()

def download_file(url, filename, headers):
    try:
        os.makedirs("downloads", exist_ok=True)
        path = os.path.join("downloads", filename)
        if os.path.exists(path):
            console.print(f"⚠️ [yellow]{filename} already exists. Skipping.[/yellow]")
            return
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        console.print(f"✅ Saved: downloads/{filename}")
    except Exception as e:
        console.print(f"❌ Failed to download {filename}: {e}")

def download_video_and_music(cookie, json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        item = data["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
        video_url = item["video"]["playAddr"]
        music_url = item["music"]["playUrl"]
        video_id = item["id"]
    except Exception as e:
        console.print(f"❌ [red]Video not found in JSON: {e}[/red]")
        return False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Cookie": cookie,
        "Referer": "https://www.tiktok.com/",
        "Origin": "https://www.tiktok.com",
        "Accept": "*/*",
        "Range": "bytes=0-",
        "Cache-Control": "max-age=2592000"
    }

    console.print("📥 Downloading video and music...")
    download_file(video_url, f"{video_id}.mp4", headers)
    download_file(music_url, f"{video_id}.mp3", headers)
    return True