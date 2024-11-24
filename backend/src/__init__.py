from flask import Flask, jsonify
from flask_cors import CORS
from src.api.options_positions import options_positions_api

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for the entire app
    CORS(app)

    # Register Blueprints
    app.register_blueprint(options_positions_api)

    return app
