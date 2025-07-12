
import os
import json
import requests
from bs4 import BeautifulSoup

from rich.console import Console

console = Console()


def dump_tiktok_json(url: str, headers: dict, filename: str = "tiktok_dump.json") -> bool:
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        console.print(f"❌ [red]Failed to fetch HTML. Status Code: {res.status_code}[/red]")
        return False

    soup = BeautifulSoup(res.text, "html.parser")
    script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})

    if not script_tag:
        console.print("🥲 [yellow]JSON script tag not found. Trying fallback.[/yellow]")
        return False

    try:
        data = json.loads(script_tag.string)
        os.makedirs("dump", exist_ok=True)
        with open(f"dump/{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        console.print(f"✅ [green]JSON saved to dump/{filename}[/green]")
        return True
    except Exception as e:
        console.print(f"❌ [red]Failed to parse JSON: {e}[/red]")
        return False