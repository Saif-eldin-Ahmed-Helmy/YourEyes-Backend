# YourEyes-Backend

This repository contains the Flask-based backend server for the YourEyes application, designed to assist visually impaired users. It provides a suite of AI-powered services through a RESTful API, including image analysis, text extraction, and speech synthesis.

## Features

- **Clothing & Scene Analysis:** Utilizes semantic segmentation and the Gemini API to identify clothing items, colors, and other details in an image, such as whether people are wearing glasses and their hair color. It provides a structured JSON response and a summary in Egyptian Arabic.
- **Image Description:** Generates a descriptive caption for an image using the BLIP model and translates it into Arabic.
- **Optical Character Recognition (OCR):** Extracts text from images (supporting English and Arabic) using Tesseract and from various document formats (PDF, DOCX) using Textract.
- **Text-to-Speech (TTS):** Converts Arabic text into audible speech, delivering it as a WAV audio file.
- **Translation:** Translates text from English to Arabic using a fine-tuned Helsinki-NLP model.
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
