# Universal Video Downloader

A simple web-based video downloader powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [FastAPI](https://fastapi.tiangolo.com/).

## Features

- **Platform Support**: YouTube, Bilibili, TikTok, Douyin, and many others supported by yt-dlp.
- **Web Interface**: Clean, responsive UI built with Tailwind CSS.
- **Mobile Compatible**: Works on iOS and Android browsers.
- **Simple Workflow**: Paste link -> Parse -> Download.

## Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (Optional, but highly recommended for best video quality merging)

## Installation

1. Clone the repository or download the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

1. Start the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2. Open your browser and navigate to:
   - Local: `http://localhost:8000`
   - Network (for mobile): `http://<YOUR_PC_IP>:8000`

## Mobile Usage

1. Ensure your phone and computer are on the same Wi-Fi.
2. Access the web page using your computer's IP address.
3. Paste the video link and click "Parse".
4. Click "Download Video".
   - **iOS (Safari)**: Tap the download icon in the address bar, open the file, tap "Share", then "Save Video".
   - **Android**: File will download to your "Downloads" folder. Open it and view/move to Gallery.

## Notes

- **FFmpeg**: If FFmpeg is not installed, the downloader will fallback to the best available single-file format (which might be 720p or lower on YouTube). For 1080p+ with audio, please install FFmpeg and add it to your system PATH.
