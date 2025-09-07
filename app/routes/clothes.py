from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import torch
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
import requests
import base64

# Blueprint
clothes_bp = Blueprint('clothes_bp', __name__)

# Load model and processor
model_name = "mattmdjaga/segformer_b2_clothes"
processor = SegformerImageProcessor.from_pretrained(model_name)
model = AutoModelForSemanticSegmentation.from_pretrained(model_name)
model.eval()

# Gemini API constants
API_KEY = "AIzaSyDPqsG_AFgOBtywBpwu8qWt-eB8z8mVQhk"
BASE_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key="

@clothes_bp.route('/clothes', methods=['POST'])
def segment_and_analyze_clothes():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        image_bytes = np.frombuffer(image_file.read(), np.uint8)
        orig_bgr = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        if orig_bgr is None:
            return jsonify({'error': 'Invalid image file'}), 400

        h_orig, w_orig = orig_bgr.shape[:2]
        rgb = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2RGB)

        # Preprocess for Segformer
        inputs = processor(images=rgb, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        upsampled_logits = torch.nn.functional.interpolate(logits, size=(h_orig, w_orig), mode='bilinear', align_corners=False)
        pred = upsampled_logits.argmax(dim=1)[0].cpu().numpy().astype(np.uint8)

        # Filter by confidence
        probs = torch.nn.functional.softmax(upsampled_logits, dim=1)[0]
        confidence, _ = torch.max(probs, dim=0)
        confidence_mask = (confidence >= 0.5).cpu().numpy()
        pred[~confidence_mask] = 0

        # Keep only relevant clothing classes
        clothing_ids_of_interest = [2, 4, 6, 11, 14, 15]
        clothing_mask = np.isin(pred, clothing_ids_of_interest)
        masked_image = np.zeros_like(orig_bgr)
        masked_image[clothing_mask] = orig_bgr[clothing_mask]

        # Convert to JPEG and encode as base64
        _, encoded_image = cv2.imencode('.jpg', masked_image)
        image_base64 = base64.b64encode(encoded_image.tobytes()).decode('utf-8')

        # Build Gemini-compatible prompt
        gemini_prompt = (
            "Analyze the image to identify all visible clothing items. For each item, determine its type and color.\n\n"
            "If the image contains one or more individuals, please also identify:\n"
            "- For each person, whether they are wearing glasses (true/false).\n"
            "- For each person, their visible hair color (if they're bald don't mention their hair color).\n\n"
            "Structure your response as a JSON object.\n\n"
            "- If one or more people are present, create a top-level key for each person (e.g., \"person1\", \"person2\"). "
            "The value for each person key should be another JSON object containing the keys \"clothing\" (with a value being a JSON object of \"clothing_type\": \"color\" pairs), \"glasses\" (true/false), and \"hair_color\" (\"color\").\n"
            "- If there are clothing items visible that are not being worn by any person, create a top-level key named \"other_clothing\". The value for this key should be a JSON object of \"clothing_type\": \"color\" pairs.\n"
            "- Include a top-level key named \"summary_egyptian_arabic\" with a short, descriptive summary of the scene in Egyptian Arabic, including hair color.\n"
            "- Don't mention in the arabic summary that this is an image.\n"
            "- If the image quality is too poor to discern clothing items or people, respond with the single word \"BAD\".\n"
        )

        # Gemini API payload
        payload = {
            "contents": [
                {
                    "parts": [
                        { "text": gemini_prompt },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            BASE_API_URL + API_KEY,
            headers={"Content-Type": "application/json"},
            json=payload
        )

        if response.status_code != 200:
            print("Gemini error:", response.text)
            return jsonify({'error': 'Gemini API failed'}), 500

        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500
