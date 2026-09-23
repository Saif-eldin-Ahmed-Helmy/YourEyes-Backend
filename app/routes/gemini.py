"""Local image-analysis gateway used by the Unity application."""
import os
import re

import requests
from flask import Blueprint, jsonify, request

bp = Blueprint('gemini', __name__)


@bp.route('/gemini/generate', methods=['POST'])
def generate():
    # The development gateway accepts native clients on the local machine.
    if request.remote_addr not in ('127.0.0.1', '::1') or request.headers.get('Origin'):
        return jsonify(error='Local clients only'), 403
    key = os.environ.get('GOOGLE_GEMINI_API_KEY', '')
    model = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
    if not key or not re.fullmatch(r'[A-Za-z0-9._-]+', model):
        return jsonify(error='Image analysis is not configured'), 503
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get('contents'), list) or not payload['contents']:
        return jsonify(error='Expected image-analysis contents'), 400
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
            headers={'x-goog-api-key': key},
            json={'contents': payload['contents']},
            timeout=30,
        )
        if response.status_code != 200:
            return jsonify(error='Image analysis is temporarily unavailable'), 502
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get('candidates'), list):
            return jsonify(error='Unexpected image-analysis response'), 502
        return jsonify(candidates=body['candidates'])
    except (requests.RequestException, ValueError):
        return jsonify(error='Image analysis is temporarily unavailable'), 502
