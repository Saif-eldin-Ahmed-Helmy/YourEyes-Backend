# YourEyes-Backend

This repository contains a Flask prototype for the [YourEyes Unity client](https://github.com/Saif-eldin-Ahmed-Helmy/YourEyes). It connects image description, clothing segmentation, translation, OCR, speech synthesis, and a simple hardware-command mailbox. The source is provided for review; a clean full-model startup has not been verified.

## Current status and setup

- The app registers `POST /describe`, `POST /clothes`, `POST /translate`, `POST /tts`, `POST /read`, and `GET`/`POST /command`. `GET /hello` is a smoke endpoint.
- The provider key for `/clothes` must be supplied as `GOOGLE_GEMINI_API_KEY` in the **server environment**. It is not committed. The route returns 503 if the key is missing.
- This checkout has no pinned dependency lockfile or model assets. Its Python imports require Flask, PyTorch, Transformers, OpenCV, NumPy, Pillow, Requests, pytesseract, textract, gTTS, and miniaudio. OCR also needs a Tesseract installation; model code downloads public pretrained checkpoints at import time. Install and validate those dependencies for your platform before attempting a full run.
- The development entry point is `python "YourEyes Backend (Flask).py"`. It binds to `127.0.0.1:5000` by default with the debugger disabled. `HOST` can change the bind address. The command mailbox has no authentication; do not expose this prototype on a public interface.
- The lightweight route checks run without model downloads: create a Python environment, install Flask, then run `python -m unittest discover -s tests -v`.

The API and model paths have not been evaluated for accessibility outcomes, latency, or production reliability. The Unity repository is a partial source export with external package/model prerequisites.

## Features

- **Clothing & Scene Analysis:** Utilizes semantic segmentation and the Gemini API to identify clothing items, colors, and other details in an image, such as whether people are wearing glasses and their hair color. It provides a structured JSON response and a summary in Egyptian Arabic.
- **Image Description:** Generates a descriptive caption for an image using the BLIP model and translates it into Arabic.
- **Optical Character Recognition (OCR):** Extracts text from images (supporting English and Arabic) using Tesseract and from various document formats (PDF, DOCX) using Textract.
- **Text-to-Speech (TTS):** Converts Arabic text into audible speech, delivering it as a WAV audio file.
- **Translation:** Loads a public pretrained Helsinki-NLP English-to-Arabic model. Fine-tuning is not evidenced in this repository.
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
