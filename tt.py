import argparse
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.progress import Progress
from time import sleep

from core.getHeaders import get_tiktok_headers
from core.dump import dump_tiktok_json
from core.video import download_video_and_music
from core.photo import download_tiktok_photos

console = Console()

def print_intro():
    console.print(Panel.fit(
        "[bold blue]TIKDLY — TikTok Downloader[/bold blue]\n"
        "[white]Author :[/white] [bold green]github.com/rizxyu[/bold green]\n"
        "[white]Version:[/white] 0.0.2\n"
        "[white]Report :[/white] Found bug? [bold cyan][link=https://github.com/rizxyu/Tikdly-Python/issues]Open an issue on GitHub[/link][/bold cyan]",
        title="[bold yellow]TIKDLY[/bold yellow]",
        border_style="cyan"
    ))


# === CLI entry ===
if __name__ == "__main__":
    print_intro()
    parser = argparse.ArgumentParser(description="TIKDLY: TikTok Downloader CLI")
    parser.add_argument("--url", type=str, help="TikTok post URL")
    args = parser.parse_args()

    if args.url:
        tiktok_url = args.url.strip()
    else:
        tiktok_url = input("📎 Enter TikTok URL: ").strip()

    with console.status("[bold cyan]Getting TikTok headers...") as status:
        headers = get_tiktok_headers(tiktok_url)
        sleep(0.5)

    with console.status("[bold cyan]Dumping TikTok JSON...") as status:
        dump_success = dump_tiktok_json(tiktok_url, headers)
        sleep(0.5)

    if dump_success:
        with console.status("[bold cyan]Downloading video and music...") as status:
            success = download_video_and_music(headers['Cookie'], "dump/tiktok_dump.json")
            sleep(0.5)
        if not success:
            console.print("📸 Falling back to photo downloader...\n")
            with console.status("[bold cyan]Downloading photos...") as status:
                download_tiktok_photos(tiktok_url)
                sleep(0.5)
    else:
        console.print("📸 Fallback triggered due to failed JSON. Trying photo downloader...\n")
        with console.status("[bold cyan]Downloading photos...") as status:
            download_tiktok_photos(tiktok_url)
            sleep(0.5)
