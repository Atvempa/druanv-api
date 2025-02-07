from flask import jsonify, request
from app import app, profiles
from langchain_openai import OpenAIEmbeddings
import os

# Initialize LangChain embeddings
embeddings = OpenAIEmbeddings(
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model="text-embedding-ada-002"
)

@app.route('/users/<email>', methods=['GET'])
def get_user(email):
    try:
        user = profiles.find_one({'email': email}, {'_id': 0})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['PUT'])
def update_user():
    try:
        data = request.get_json()
        if 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
            
        result = profiles.update_one(
            {'email': data['email']},
            {'$set': data},
            upsert=True
        )
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        search_text = data.get('search_text')
        if not search_text:
            return jsonify({'error': 'Search text is required'}), 400
            
        # Generate embedding for search text
        query_embedding = embeddings.embed_query(search_text)
        
        # Search using MongoDB vector search
        results = profiles.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": data.get('num_candidates', 10),
                    "limit": data.get('top_n', 3)
                }
            },
            {
                "$addFields": {
                    "score": {"$meta": "vectorSearchScore"}
                }
            },
            {
                "$project": {
                    "_id": 0
                }
            }
        ])
        
        return jsonify(list(results))
    except Exception as e:
        return jsonify({'error': str(e)}), 500 