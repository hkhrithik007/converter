# Media Converter (Image + Video)

A clean, responsive web app to convert images and videos through a simple web UI. Built with Flask, Pillow, and MoviePy. The interface features a centered card layout, high-contrast typography, and optional decorative background images.

## Features
- Image conversion: PNG, JPG, BMP, GIF, TIFF, WEBP, ICO.
- Video conversion: MP4, AVI, MOV, WEBM, animated GIF.
- Two-tab interface: Image Converter and Video Converter.
- Direct download of converted files.
- Modern, accessible design.

## Project Structure
```
project-root/
├─ app.py
├─ requirements.txt
├─ templates/
│  └─ index.html
└─ README.md
```

## Requirements
- Python 3.9+ (tested with 3.10+)
- FFmpeg installed and available on PATH (required for video conversions)

Install FFmpeg:
- macOS: brew install ffmpeg
- Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y ffmpeg
- Windows: Download FFmpeg and add its bin directory to PATH

Verify: ffmpeg -version

## Setup
1) Clone
```
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2) Create and activate a virtual environment
- macOS/Linux
```
python3 -m venv .venv
source .venv/bin/activate
```
- Windows
```
python -m venv .venv
.\.venv\Scripts\activate
```

3) Install dependencies
```
pip install -r requirements.txt
```

Example requirements.txt:
```
Flask==3.1.0
Pillow==11.3.0
moviepy==2.2.1
gunicorn==22.0.0
```

4) Run (development)
```
python app.py
```
Open http://127.0.0.1:5000/

## Usage
- Image tab: upload an image and choose output format (PNG/JPG/BMP/GIF/TIFF/WEBP/ICO).
- Video tab: upload a video and choose output format (MP4/AVI/MOV/WEBM/GIF).
- Click Convert to download the converted file.

## Deployment
- Use any Python-capable host (e.g., Render, Railway, Fly.io, a VPS, or a Docker environment).
- Ensure FFmpeg is installed in the runtime environment.
- Example production start command:
```
gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app
```

Optional Dockerfile outline:
```
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD ["gunicorn","-w","2","-k","gthread","-b","0.0.0.0:8080","app:app"]
```

## Configuration (optional)
- Set a maximum upload size in Flask if desired:
```
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB
```

## Customization
- Add/remove formats by editing the <select> elements in templates/index.html.
- Adjust quality/compression (e.g., JPEG/WebP quality, PNG optimization) or video parameters (bitrate, resolution, fps) in the backend routes.
- Replace or remove the randomized background image layer in the template.

## License
Choose a license (e.g., MIT) and include it as LICENSE.

## Acknowledgments
- Flask (Pallets Projects)
- Pillow (PIL fork)
- MoviePy and FFmpeg

## Contributing
- Fork the repo, create a branch, and open a PR with clear description and testing notes.

Sources
