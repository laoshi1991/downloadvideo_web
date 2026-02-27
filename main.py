from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid
import shutil

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Temporary directory for downloads
DOWNLOAD_DIR = "temp_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

class VideoRequest(BaseModel):
    url: str
    cookie: str = None

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/info")
async def get_video_info(video_request: VideoRequest):
    url = video_request.url
    cookie = video_request.cookie
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'dump_single_json': True,
        }
        
        # Add headers if cookie is provided
        if cookie:
            ydl_opts['http_headers'] = {'Cookie': cookie}
            # For Bilibili, sometimes User-Agent is also needed with Cookie
            if "bilibili.com" in url:
                ydl_opts['http_headers']['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ydl_opts['http_headers']['Referer'] = 'https://www.bilibili.com/'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract relevant info
            formats = []
            for f in info.get('formats', []):
                # Filter for useful formats (mp4, with video and audio if possible)
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                     formats.append({
                        'format_id': f['format_id'],
                        'ext': f['ext'],
                        'resolution': f.get('resolution', 'Unknown'),
                        'filesize': f.get('filesize', 0),
                        'note': f.get('format_note', '')
                    })
            
            # If no combined formats found, just take the best one
            if not formats:
                 formats.append({
                    'format_id': 'best',
                    'ext': 'mp4',
                    'resolution': 'Best Quality',
                    'filesize': 0,
                    'note': 'Best available'
                })

            return {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "formats": formats
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error cleaning up file {path}: {e}")

@app.get("/api/download")
async def download_video(url: str, format_id: str = "best", cookie: str = None, background_tasks: BackgroundTasks = BackgroundTasks()):
    try:
        file_id = str(uuid.uuid4())
        filename_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': filename_template,
            'quiet': True,
            'no_warnings': True,
        }

        # Add headers if cookie is provided
        if cookie:
            ydl_opts['http_headers'] = {'Cookie': cookie}
            if "bilibili.com" in url:
                ydl_opts['http_headers']['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ydl_opts['http_headers']['Referer'] = 'https://www.bilibili.com/'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        if not os.path.exists(filename):
             raise HTTPException(status_code=500, detail="File not found after download")

        # Schedule cleanup
        background_tasks.add_task(cleanup_file, filename)
        
        return FileResponse(
            path=filename, 
            filename=os.path.basename(filename),
            media_type='application/octet-stream'
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
