from gettext import translation
from flask import Blueprint, request, jsonify
from PIL import Image
import io
from transformers import BlipProcessor, BlipForConditionalGeneration
from app.services.translation_service import translate

# Blueprint for image description
describe_bp = Blueprint('describe_bp', __name__)

# Load the BLIP processor and model once at startup
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@describe_bp.route('/describe', method3s=['POST'])
def describe_image():
    """
    Expects a multipart/form-data POST with an 'image' file.
    Returns a JSON response with the generated caption:
        { "caption": "..." }
    """
    # Check for uploaded file
    if 'image' not in request.files:
        return jsonify({'error': 'Image file is required under the "image" key'}), 400

    file = request.files['image']
    try:
        # Read image into PIL
        image = Image.open(io.BytesIO(file.read())).convert('RGB')

        # Prepare inputs for the BLIP model
        inputs = processor(images=image, return_tensors="pt")

        # Generate caption
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        translation = translate(caption)


        # Return the caption
        return jsonify({'caption': translation}), 200

    except Exception as e:
        # Handle errors in processing or model inference
        return jsonify({'error': str(e)}), 500
