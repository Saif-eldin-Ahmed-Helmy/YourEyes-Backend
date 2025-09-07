from flask import Blueprint, request, jsonify
from PIL import Image
import io
import cv2
import pytesseract
import numpy as np
import textract
import tempfile
import os

# Configure Tesseract executable path once at startup
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Blueprint for OCR services
ocr_bp = Blueprint('ocr_bp', __name__)

@ocr_bp.route('/read', methods=['POST'])
def read_content():
    """
    Single endpoint for OCR and document text extraction.
    Expects multipart/form-data POST with either:
      - 'image': image file for Tesseract OCR
        - optional 'lang': 'eng' (default) or 'ara'
      - OR 'file': document (PDF, docx, etc.) for Textract
    Returns JSON:
      { 'text': '...' }
    """
    # Determine mode based on uploaded key
    if 'image' in request.files:
        file = request.files['image']
        lang = request.form.get('lang', 'eng')
        try:
            # Read image bytes into OpenCV
            img_bytes = file.read()
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Rotate, grayscale, sharpen
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            sharp = cv2.filter2D(gray, -1, kernel)

            # OCR via Tesseract
            if lang == 'eng':
                text = pytesseract.image_to_string(sharp)
            else:
                config = r'--psm 3 --oem 3 -l ara'
                text = pytesseract.image_to_string(sharp, config=config)

            if not text.strip():
                return jsonify({'text': 'there is no any text to read'}), 200

            return jsonify({'text': text.strip()}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif 'file' in request.files:
        file = request.files['file']
        try:
            # Save to temporary file for Textract
            data = file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
                tmp.write(data)
                tmp_path = tmp.name

            text = textract.process(tmp_path, language='eng').decode('utf-8')
            os.remove(tmp_path)

            if not text.strip():
                return jsonify({'text': 'there is no any text to read'}), 200

            return jsonify({'text': text.strip()}), 200

        except Exception as e:
            try:
                if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)
            except: pass
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'No valid upload found; please include either "image" or "file"'}), 400
