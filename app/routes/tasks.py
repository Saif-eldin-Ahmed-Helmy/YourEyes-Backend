from flask import Flask, Blueprint, request, jsonify
import json

app = Flask(__name__)

# Variable to store the last command
last_command = None

# Blueprint for receiving ESP32 commands
tasks_bp = Blueprint('tasks_bp', __name__)

# Route for receiving commands
@tasks_bp.route('/command', methods=['POST'])
def receive_command():
    """
    Expects JSON: { "key": <int>, "distance": <float, optional> }
    Stores the command and sends a response to confirm.
    """
    global last_command
    data = request.get_json()
    if not data or 'key' not in data:
        return jsonify({'error': 'Field "key" is required'}), 400

    # Store the last command
    last_command = data

    return jsonify({'status': 'ok'}), 200

# Route to get the last command and clear it after sending
@tasks_bp.route('/command', methods=['GET'])
def get_last_command():
    """
    Returns the last stored command as JSON, clears it after sending.
    """
    global last_command
    if last_command is None:
        return jsonify({'error': 'No command received yet'}), 404

    # Store the current command to send, then clear it
    command_to_send = last_command
    last_command = None

    return jsonify(command_to_send), 200