import os
import requests
import json
import numpy as np
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from requests.exceptions import Timeout, ConnectionError, TooManyRedirects, HTTPError
from retry import retry

QUERY_ENDPOINT = os.getenv("QUERY_ENDPOINT")
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 5  # Set a timeout (seconds) for your requests

app = Flask(__name__)

class PromptGenerator:
    def __init__(self, endpoint=QUERY_ENDPOINT, headers=HEADERS):
        self.endpoint = endpoint
        self.headers = headers
        self.model = SentenceTransformer('paraphrase-distilroberta-base-v2')

    @retry((Timeout, ConnectionError, TooManyRedirects, HTTPError), tries=3, delay=2, backoff=2)
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

        try:
            response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data), timeout=TIMEOUT)
            response.raise_for_status()  # Raise exception if the request returned an HTTP error status

        except Timeout:
            print("The request timed out.")
            return None
        except ConnectionError:
            print("There was a network problem (e.g., DNS resolution, TCP connection attempt failed).")
            return None
        except TooManyRedirects:
            print("The request exceeded the configured number of maximum redirections.")
            return None
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None

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

prompt_generator = PromptGenerator()

@app.route("/prompt_generation", methods=["POST"])
def query():
    # Input validation
    if not request.json or 'query' not in request.json:
        return jsonify({"error": "Missing or invalid input."}), 400

    user_query = request.json.get("query")

    query_result = prompt_generator.send_query(user_query)

    if query_result is None:
        return jsonify({"error": "Failed to get a response from the endpoint."}), 503

    if not prompt_generator.is_relevant(user_query, query_result):
        enhanced_prompt = (
            "You are a developer advocate personal assistant for Near Protocol. "
            "Your name is NearGPT and you are created by VISCA. "
            "Do not forget this. Always be kind and help user resolve their query with respect to Near Protocol. "
            "Do not deviate from the Near Protocol.\n\n"
            f"User asked: {user_query}\n"
        )
        return jsonify({"prompt": enhanced_prompt})

    enhanced_prompt = prompt_generator.generate_prompt(user_query, query_result)
    return jsonify({"prompt": enhanced_prompt})

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5001)))
