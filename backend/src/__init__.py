from flask import Flask
from flask_cors import CORS
from src.api.options_positions import options_positions_api, initialize_options_positions

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for the entire app
    CORS(app)

    # Register Blueprints
    app.register_blueprint(options_positions_api)

    # Initializes the list with the locally stored options information
    initialize_options_positions()

    return app
