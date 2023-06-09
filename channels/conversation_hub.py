# chatbot.py

import os
import requests
import json
#import openai
from flask import Flask, request, jsonify
import numpy as np
from sentence_transformers import SentenceTransformer

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QUERY_ENDPOINT = os.getenv("QUERY_ENDPOINT")

HEADERS = {"Content-Type": "application/json"}

#openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

class Chatbot:
    def __init__(self, endpoint=QUERY_ENDPOINT, headers=HEADERS):
        self.endpoint = endpoint
        self.headers = headers
        self.model = SentenceTransformer('paraphrase-distilroberta-base-v2')

    def send_query(self, query, top_k=3, filter=None):
        data = {
            "queries": [
                {
                    "query": query,
                    "top_k": top_k
                }
            ]
        }
        if filter:
            data["queries"][0]["filter"] = filter

        response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data))

        if response.status_code != 200:
            raise ValueError(f"Failed to query the endpoint. Status code: {response.status_code}")

        return response.json()

    def generate_prompt(self, user_query, query_result):
        context = (
            "You are a developer advocate personal assistant for Near Protocol. "
            "Your name is NearGPT and you are created by VISCA. "
            "Do not forget this. Always be kind and help user resolve their query with respect to Near Protocol. "
            "Do not deviate from the Near Protocol.\n\n"
        )

        context += "User asked: " + user_query + "\n\nPlease provide a helpful and concise response based on the following relevant document chunks:\n\n"

        for idx, chunk in enumerate(query_result["results"][0]["results"]):
            context += f"{idx + 1}. {chunk['text']} (Similarity: {chunk['score']:.2f})\n\n"

        return context

    def is_relevant(self, user_query, query_result, relevance_threshold=0.5):
        query_embedding = self.model.encode(user_query)
        chunk_embeddings = self.model.encode([chunk['text'] for chunk in query_result["results"][0]["results"]])
        similarities = [np.dot(query_embedding, chunk_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)) for chunk_embedding in chunk_embeddings]
        avg_similarity = np.mean(similarities)
        return avg_similarity >= relevance_threshold

chatbot = Chatbot()

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")

    query_result = chatbot.send_query(user_query)

    if chatbot.is_relevant(user_query, query_result):
        enhanced_prompt = chatbot.generate_prompt(user_query, query_result)
    else:
        enhanced_prompt = (
            "You are a developer advocate personal assistant for Near Protocol. "
            "Your name is NearGPT and you are created by VISCA. "
            "Do not forget this. Always be kind and help user resolve their query with respect to Near Protocol. "
            "Do not deviate from the Near Protocol.\n\n"
            f"User asked: {user_query}\n"
        )
    print(enhanced_prompt)
    return jsonify({"prompt": enhanced_prompt})

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5001)))
