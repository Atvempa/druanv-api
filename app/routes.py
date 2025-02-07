from flask import jsonify, request
from app import app
from app.services.profile_service import ProfileService
import logging

profile_service = ProfileService()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User Profile endpoints
@app.route('/api/users/<email>', methods=['GET'])
def get_user_profile(email):
    try:
        profile = profile_service.get_user_profile(email)
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/users', methods=['PUT'])
def update_user_profile():
    try:
        profile_data = request.get_json()
        result = profile_service.update_user_profile(profile_data)
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Search endpoints
@app.route('/api/search', methods=['POST'])
def search_profiles():
    try:
        logger.info("Received search request")
        data = request.get_json()
        logger.info(f"Request data: {data}")
        search_text = data.get('search_text', '')
        top_n = data.get('top_n', 3)
        num_candidates = data.get('num_candidates', 10)
        
        logger.info(f"Search request received: {search_text}")
        
        results = profile_service.get_search_results(
            search_text, 
            top_n=top_n, 
            num_candidates=num_candidates
        )
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/search/keywords', methods=['POST'])
def extract_keywords():
    try:
        text = request.get_json().get('text', '')
        keywords = profile_service.get_keywords(text)
        return jsonify(keywords), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 