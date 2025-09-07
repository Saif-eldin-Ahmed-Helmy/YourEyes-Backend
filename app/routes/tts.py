from flask import Blueprint, request, send_file, jsonify
from app.services.tts_service import synthesize_speech

tts_bp = Blueprint('tts_bp', __name__)

@tts_bp.route('/tts', methods=['POST'])
def tts():
    data = request.get_json(force=True) or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    try:
        audio_io = synthesize_speech(text)
        return send_file(
            audio_io,
            mimetype='audio/wav',
            download_name='tts.wav',
            as_attachment=False
        )
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
