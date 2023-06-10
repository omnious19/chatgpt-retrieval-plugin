import requests
from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

VISCA_ENGINE_API_URL = os.environ.get("VISCA_ENGINE_API_URL")
VISCA_HUB_API_TOKEN = os.environ.get("VISCA_HUB_API_TOKEN")
VISCA_HUB_ACCESS_TOKEN = os.environ.get("VISCA_HUB_ACCESS_TOKEN")
VISCA_HUB_ACCOUNT_ID = os.environ.get("VISCA_HUB_ACCOUNT_ID")
VISCA_HUB_BASE_URL = os.environ.get("VISCA_HUB_BASE_URL")


@app.route("/webhook", methods=["POST"])
def webhook():
    if not request.is_json:
        return jsonify({"error": "Invalid request"}), 400

    data = request.json

    if data.get("event") == "message_created" and not data["sender"].get("is_bot") and data["sender"].get("type") != "agent_bot":
        user_id = data["sender"]["id"]
        user_message = data.get("content")
        conversation_id = data["conversation"]["id"]

        # Pass the message to the Visca_Engine agent
        try:
            agent_response = ask_visca_engine(user_id, user_message)
        except Exception as e:
            logging.error(f"Error querying Visca_Engine: {e}")
            return jsonify({"error": "An internal error occurred"}), 500

        # Send the agent's response back to Visca_Hub
        try:
            send_message_to_visca_hub(conversation_id, agent_response)
        except Exception as e:
            logging.error(f"Error sending message to Visca_Hub: {e}")
            return jsonify({"error": "An internal error occurred"}), 500

    return jsonify({}), 200

def ask_visca_engine(user_id, message):
    data = {
        "user_id": user_id,
        "payload": message
    }

    try:
        response = requests.post(VISCA_ENGINE_API_URL, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request to Visca_Engine failed: {e}")
        raise

    return response.json().get('response')

def send_message_to_visca_hub(conversation_id, message_content):
    url = f"{VISCA_HUB_BASE_URL}/api/v1/accounts/{VISCA_HUB_ACCOUNT_ID}/conversations/{conversation_id}/messages"
    headers = {"Content-Type": "application/json", "api_access_token": VISCA_HUB_ACCESS_TOKEN}
    data = {"content": message_content, "private": False}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request to Visca_Hub failed: {e}")
        raise

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)))  # Enable HTTPS
