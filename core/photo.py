import time
import os
import re


from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rich.console import Console
from core.video import download_file

console = Console()
def download_tiktok_photos(post_url: str):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get(post_url)
    time.sleep(5)

    console.print("🔍 Searching for photo carousel slides...")

    # Ambil semua <img> dari swiper-slide
    slides = driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide[data-swiper-slide-index] > img")
    image_map = {}

    for img in slides:
        try:
            parent = img.find_element(By.XPATH, "./..")
            index_str = parent.get_attribute("data-swiper-slide-index")
            src = img.get_attribute("src")

            if (
                index_str is not None
                and src
                and is_valid_tiktok_photo_url(src)
            ):
                index = int(index_str)
                if index not in image_map:
                    image_map[index] = src
        except Exception:
            continue

    if not image_map:
        console.print("🥲 [red]No valid photo carousel found.[/red]")
    else:
        console.print(f"📸 Found [cyan]{len(image_map)}[/cyan] photo(s). Starting download...")
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        for idx in sorted(image_map.keys()):
            url = image_map[idx]
            ext = os.path.splitext(urlparse(url).path)[-1] or ".jpg"
            filename = f"photo_{now}_{idx + 1}{ext}"
            download_file(url, filename, headers={})

        console.print("✅ [green]Photo(s) download completed.[/green]")

    # 🔊 Coba cari <audio>
    try:
        audio_element = driver.find_element(By.TAG_NAME, "audio")
        audio_src = audio_element.get_attribute("src")
        if audio_src:
            filename = f"music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            console.print("🎵 Found audio! Downloading background music...")
            download_file(audio_src, filename, headers={})
    except Exception:
        console.print("🎵 [yellow]No audio found in photo post.[/yellow]")
    driver.quit()

def is_valid_tiktok_photo_url(src: str) -> bool:
    """Validates TikTok photo URL based on known photomode pattern."""
    return bool(re.search(r"tiktokcdn\.com/.+photomode-.+\.jpeg", src))