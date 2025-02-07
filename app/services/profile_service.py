from app import mongo
from bson import json_util
import json
import certifi
from pymongo import MongoClient
from app.config import Config
from openai import OpenAI

class ProfileService:
    def __init__(self):
        # Initialize MongoDB client for vector search
        self.client = MongoClient(Config.MONGO_URI, tlsCAFile=certifi.where())
        self.db = self.client["profiles_db"]
        self.collection = self.db["profiles"]
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def get_user_profile(self, email):
        profile = mongo.db.profiles.find_one({'email': email})
        if not profile:
            raise Exception('Profile not found')
        return json.loads(json_util.dumps(profile))

    def update_user_profile(self, profile_data):
        if 'email' not in profile_data:
            raise Exception('Email is required')
        
        result = mongo.db.profiles.update_one(
            {'email': profile_data['email']},
            {'$set': profile_data},
            upsert=True
        )
        return result.modified_count > 0

    def get_search_results(self, search_text, top_n=3, num_candidates=10):
        if len(search_text) > 200:
            raise Exception('Search text exceeds 200 words limit')
        
        try:
            # Get embedding for the search text
            query_embedding = self.get_embedding(search_text)
            
            search_query = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": num_candidates,
                        "limit": top_n
                    }
                },
                {
                    "$addFields": {
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]

            results = list(self.collection.aggregate(search_query))
            return json.loads(json_util.dumps(results))
        except Exception as e:
            raise Exception(f"Error in vector search: {str(e)}")

    def get_embedding(self, text):
        """Generate embedding for a given text using OpenAI API."""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")

    def get_keywords(self, text):
        if len(text) > 200:
            raise Exception('Text exceeds 200 words limit')
        
        # Implement your keyword extraction logic here
        # This is a placeholder implementation
        keywords = []  # Add your keyword extraction logic
        return keywords 