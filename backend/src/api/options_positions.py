from flask import Blueprint, request, jsonify
from src.util.options_position import OptionsPosition

options_positions_api = Blueprint('options_positions_api', __name__)

options_positions_store = []

@options_positions_api.route('/api/options_positions', methods=['GET'])
def get_positions():
    return jsonify(options_positions_store), 200

@options_positions_api.route('/api/options_positions', methods=['POST'])
def add_position():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    
    # Create a new OptionsPositions instance
    new_position = OptionsPosition(**data)
    options_positions_store.append(new_position.__dict__)  # Store as a dict for simplicity
    return jsonify({'message': 'Position added successfully!'}), 201
