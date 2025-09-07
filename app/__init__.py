from flask import Flask
from .routes import translation, tts, clothes, describe, ocr, tasks  # Import your routes

def create_app():
    app = Flask(__name__)

    # Register blueprints for modular routes
    app.register_blueprint(translation.bp)
    app.register_blueprint(tts.tts_bp)
    app.register_blueprint(clothes.clothes_bp)
    app.register_blueprint(describe.describe_bp)
    app.register_blueprint(ocr.ocr_bp)
    app.register_blueprint(tasks.tasks_bp)

    return app