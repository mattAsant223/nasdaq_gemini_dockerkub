# app/__init__.py
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

