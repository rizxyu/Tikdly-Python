import time
import os
import json

from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from rich.console import Console

console = Console()


def get_tiktok_headers(url: str) -> dict:
    headers_path = "headers.txt"
    # Cek jika file headers.txt sudah ada
    if os.path.exists(headers_path):
        try:
            with open(headers_path, "r", encoding="utf-8") as f:
                headers = json.load(f)
            console.print("✅ [green]Headers loaded from headers.txt[/green]\n")
            return headers
        except Exception as e:
            console.print(f"[red]Failed to load headers.txt: {e}[/red]")
    # Jika tidak ada, ambil dari browser
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")

    driver = None
    try:
        driver = uc.Chrome(options=options)
        console.print("🌐 [bold]Opening TikTok URL to extract headers...[/bold]")
        driver.get(url)
        time.sleep(10)
        cookies = driver.get_cookies()
        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        user_agent = options.arguments[-1]
        headers = {
            "User-Agent": user_agent,
            "Cookie": cookie_string,
            "Referer": "https://www.tiktok.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }
        # Simpan ke file
        with open(headers_path, "w", encoding="utf-8") as f:
            json.dump(headers, f, ensure_ascii=False, indent=2)
        console.print("✅ [green]Headers extracted and saved to headers.txt[/green]\n")
        return headers
    except Exception as e:
        console.print(f"[red]Failed to extract headers automatically: {e}[/red]")
        # Input manual jika gagal
        console.print("[yellow]Please input your TikTok headers and cookie manually.[/yellow]")
        user_agent = input("User-Agent: ").strip()
        cookie = input("Cookie: ").strip()
        headers = {
            "User-Agent": user_agent,
            "Cookie": cookie,
            "Referer": "https://www.tiktok.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }
        # Simpan ke file
        with open(headers_path, "w", encoding="utf-8") as f:
            json.dump(headers, f, ensure_ascii=False, indent=2)
        return headers
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass