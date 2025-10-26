# 🎬 AI Reel Generator

A powerful web application that automatically creates Instagram-style reels from uploaded images and text descriptions using AI-powered text-to-speech technology (ElevenLabs) and FFmpeg.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Installation & Setup](#installation--setup)
7. [Configuration](#configuration)
8. [Usage](#usage)
9. [Processing Pipeline (End-to-End)](#processing-pipeline-end-to-end)
10. [API Endpoints](#api-endpoints)
11. [Video & TTS Details](#video--tts-details)

---

## Project Overview

**AI Reel Generator** automates short-form vertical-video (reel) creation by combining user-uploaded images with AI-generated voiceovers. The app resizes and formats videos for Instagram Reels (1080×1920), synchronizes generated audio, and outputs an MP4 ready for upload.

---

## Features

- Multi-file image upload and concatenation
- AI-powered text-to-speech using ElevenLabs
- Background processing daemon for asynchronous generation
- Simple web UI for upload and gallery (Flask templates + Bootstrap)
- Tracking of processed reels (generated_reels.txt)
- Configurable FFmpeg command for customizations (watermarks, filters)

---

## System Architecture

User Browser

\--> Flask Server (main.py)

\--> user_uploads/{UUID}/

\--> generate_process.py

\--> ElevenLabs TTS + FFmpeg

\--> static/reels/{UUID}.mp4

\-->Gallery

- **main.py**: handles web routes, file uploads, and creates the UUID folder for each submission.
- **generate_process.py**: monitors `user_uploads/` for new folders, calls the TTS function, then runs FFmpeg to create the final reel.
- **text_to_audio.py**: wraps ElevenLabs API calls and saves `audio.mp3` into the session folder.

---

## Tech Stack

- Backend: Python 3.8+, Flask
- Video Processing: FFmpeg (libx264 + aac)
- TTS: ElevenLabs API (eleven_multilingual_v2)
- Frontend: HTML5, Bootstrap 5, JavaScript
- Storage: Local filesystem (user_uploads, static/reels)

---

## Project Structure

```

AI_REEL_GENERATOR/
├── main.py # Flask web app
├── generate_process.py # Background processing daemon
├── text_to_audio.py # ElevenLabs TTS integration
├── config.py # API configuration
├── generated_reels.txt # Tracks processed reels
├── ffmpeg_command.txt # FFmpeg reference
├── static/
│ ├── reels/ # Generated videos (\*.mp4)
│ ├── css/ # Stylesheets
│ └── images/ # Static images
├── templates/
│ ├── base.html # Base template layout
│ ├── index.html # Homepage
│ ├── create.html # Upload form
│ └── gallery.html # Reel gallery
└── user_uploads/
└── [UUID]/
├── input.txt # FFmpeg concatenation list
├── desc.txt # Voiceover text
├── audio.mp3 # Generated TTS audio
└── [video files] # Uploaded media

```

Each user upload session is stored in a UUID-named folder under `user_uploads/`. `input.txt` is a FFmpeg concatenation list, `desc.txt` contains the voiceover text, and `audio.mp3` is the generated TTS output.

---

## Installation & Setup

### Prerequisites

- Python 3.8 or newer
- FFmpeg installed and available in PATH
- ElevenLabs API account and API Key

### Quick Install

1. Enter directory:

```bash
cd AI_REEL_GENERATOR
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```bash
pip install flask python-dotenv elevenlabs werkzeug
```

4. Install FFmpeg:

- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`
- Windows: download and add to PATH from https://ffmpeg.org/download.html

5. Create required directories:

```bash
mkdir -p user_uploads static/reels static/css templates
```

6. Add ElevenLabs API key to `config.py` or a `.env` file:

```python
# config.py
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"
```

or in `.env`:

```
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

---

## Configuration

- `config.py` — central place for API keys and configurable constants (UPLOAD_FOLDER, OUTPUT_FOLDER, VOICE_ID, MODEL_ID, etc.).
- `main.py` — `app.config['UPLOAD_FOLDER']` should match `user_uploads/`.
- `generate_process.py` — contains the FFmpeg command template. Customize filters, watermark, or encoding flags here.

---

## Usage

### Start the web server (development):

```bash
python main.py
```

Visit: `http://localhost:5000`

### Start the background processor (in another terminal):

```bash
python generate_process.py
```

### Create a reel via the web UI

1. Open **Create Reel** page
2. Upload one or more images
3. Enter the description text for voiceover
4. Click **Create Reel**
5. Wait (background processor will handle generation)
6. Visit **Gallery** to view or download the reel

Processing time depends on input file size and system performance.

---

## Processing Pipeline (End-to-End)

1. **Upload Phase**

   - User submits form with files and description.
   - Server creates a UUID folder under `user_uploads/`.
   - Uploaded files are saved and `input.txt` (FFmpeg list) and `desc.txt` are created.

2. **Background Processing Phase**

   - `generate_process.py` polls `user_uploads/` for unprocessed folders.
   - For each folder found:
     - Calls `text_to_audio(text, folder)` to generate `audio.mp3` using ElevenLabs.
     - Runs FFmpeg command to concatenate images and add audio.
     - Writes final file to `static/reels/{folder}.mp4` and appends the ID to `generated_reels.txt`.

3. **Delivery Phase**
   - Gallery page enumerates `static/reels/` and displays generated reels.
   - Users can playback or download the generated MP4 file.

---

## API Endpoints

- `GET /` — Home (index)
- `GET /create` — Show create form
- `POST /create` — Upload files (fields: `files[]`, `text`)
- `GET /gallery` — List generated reels

**Internal functions** (not exposed as HTTP):

- `text_to_audio(text: str, folder: str) -> str` — generates `audio.mp3` and returns its path
- `reel_generator(folder: str) -> str` — runs FFmpeg and returns output path

---

## Video & TTS Details

**FFmpeg command (reference)**

```bash
ffmpeg -f concat -safe 0 -i input.txt \
  -i audio.mp3 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p output.mp4
```
