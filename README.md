# YourEyes-Backend

This repository contains a Flask prototype for the [YourEyes Unity client](https://github.com/Saif-eldin-Ahmed-Helmy/YourEyes). It connects image description, clothing segmentation, translation, OCR, speech synthesis, and a simple hardware-command mailbox.

## Setup

- The app registers `POST /describe`, `POST /clothes`, `POST /translate`, `POST /tts`, `POST /read`, and `GET`/`POST /command`. `GET /hello` is a smoke endpoint.
- Set `GOOGLE_GEMINI_API_KEY` in the server environment for image analysis. `GEMINI_MODEL` selects the gateway model (default: `gemini-2.5-flash`). Unity uses `POST /gemini/generate` at `http://127.0.0.1:5000`, with a `contents` request and `candidates` response.
- The Python dependencies are Flask, PyTorch, Transformers, OpenCV, NumPy, Pillow, Requests, pytesseract, textract, gTTS, and miniaudio. OCR also needs a Tesseract installation; model code downloads public pretrained checkpoints at import time. Install and validate those dependencies for your platform before attempting a full run.
- The development entry point is `python "YourEyes Backend (Flask).py"`. It binds to `127.0.0.1:5000` by default with the debugger disabled. `HOST` can change the bind address.
- The lightweight route checks run without model downloads: create a Python environment, install Flask, then run `python -m unittest discover -s tests -v`.

The companion Unity repository contains prototype scripts with external package and model prerequisites.

## Features

- **Clothing & Scene Analysis:** Utilizes semantic segmentation and the Gemini API to identify clothing items, colors, and other details in an image, such as whether people are wearing glasses and their hair color. It provides a structured JSON response and a summary in Egyptian Arabic.
- **Image Description:** Generates a descriptive caption for an image using the BLIP model and translates it into Arabic.
- **Optical Character Recognition (OCR):** Extracts text from images (supporting English and Arabic) using Tesseract and from various document formats (PDF, DOCX) using Textract.
- **Text-to-Speech (TTS):** Converts Arabic text into audible speech, delivering it as a WAV audio file.
- **Translation:** Loads a public pretrained Helsinki-NLP English-to-Arabic model.
- **Hardware Command Interface:** Simple endpoints to receive and retrieve commands, designed for interaction with external hardware like an ESP32.

## Technologies Used

- **Framework:** Flask
- **Machine Learning & AI:**
    - `transformers` (Hugging Face) for various models (BLIP, SegFormer, MarianMT)
    - `PyTorch`
    - Google Gemini API
    - `pytesseract` for OCR
    - `gTTS` for Text-to-Speech
- **Image & Audio Processing:**
    - `OpenCV`
    - `Pillow`
    - `miniaudio`
- **Document Processing:** `textract`
