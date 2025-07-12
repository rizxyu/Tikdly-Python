import time


from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from rich.console import Console

console = Console()


def get_tiktok_headers(url: str) -> dict:
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")

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

    driver.quit()
    console.print("✅ [green]Headers extracted successfully.[/green]\n")
    return headers