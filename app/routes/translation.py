from flask import Blueprint, request, jsonify
from app.services.translation_service import translate  # Import translation service

bp = Blueprint('translation', __name__)

@bp.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    input_text = data.get('text')
    translation = translate(input_text)  # Call the translation service
    return jsonify({"translation": translation})