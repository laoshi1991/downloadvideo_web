#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "Starting Video Downloader..."
echo "Access the website at: http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
