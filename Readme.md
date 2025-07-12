# Tikdly-Python

Easiest way to download videos, images, and music from TikTok.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rizxyu/Tikdly-Python.git
   cd Tikdly-Python
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Via Command Line

1. **Run the program**
   ```bash
   python tt.py --url "https://www.tiktok.com/@username/video/1234567890"
   ```
   Or without arguments, you will be prompted to input the URL:
   ```bash
   python tt.py
   ```

2. **Downloaded files** will be saved in the `downloads/` folder (video, music, photos) and JSON data in the `dump/` folder.

### Features

- Download TikTok videos (with music)
- Download TikTok photo carousels
- Download music from TikTok posts
- Automatic fallback to photo mode if video is not found

### Notes

- Make sure Google Chrome is installed on your system.
- If you encounter errors related to browser/driver, try updating `undetected-chromedriver` and `selenium`.