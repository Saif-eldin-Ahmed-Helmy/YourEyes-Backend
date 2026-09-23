from flask import Flask
from .routes import translation, tts, clothes, describe, ocr, tasks, gemini

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

    # Register blueprints for modular routes
    app.register_blueprint(translation.bp)
    app.register_blueprint(tts.tts_bp)
    app.register_blueprint(clothes.clothes_bp)
    app.register_blueprint(describe.describe_bp)
    app.register_blueprint(ocr.ocr_bp)
    app.register_blueprint(tasks.tasks_bp)
    app.register_blueprint(gemini.bp)

    return app
