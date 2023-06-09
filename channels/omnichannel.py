import requests
from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DEEPPAVLOV_API_URL = "https://4242-onchainengineer-vina-hepphrcg7sx.ws-us99.gitpod.io"
CHATWOOT_API_TOKEN = os.getenv("CHATWOOT_API_TOKEN")
CHATWOOT_ACCESS_TOKEN ="PM2mRAafchukkjaA3eHdCTyJ"
CHATWOOT_ACCOUNT_ID ="2"
CHATWOOT_BASE_URL ="https://hub.visca.ai"


@app.route("/webhook", methods=["POST"])
def webhook():
    if not request.is_json:
        return jsonify({"error": "Invalid request"}), 400

    data = request.json

    if data.get("event") == "message_created" and not data["sender"].get("is_bot") and data["sender"].get("type") != "agent_bot":
        user_id = data["sender"]["id"]
        user_message = data.get("content")
        conversation_id = data["conversation"]["id"]

        # Pass the message to the DeepPavlov agent
        try:
            agent_response = ask_deeppavlov(user_id, user_message)
        except Exception as e:
            logging.error(f"Error querying DeepPavlov: {e}")
            return jsonify({"error": "An internal error occurred"}), 500

        # Send the agent's response back to Chatwoot
        try:
            send_message_to_chatwoot(conversation_id, agent_response)
        except Exception as e:
            logging.error(f"Error sending message to Chatwoot: {e}")
            return jsonify({"error": "An internal error occurred"}), 500

    return jsonify({}), 200

def ask_deeppavlov(user_id, message):
    data = {
        "user_id": user_id,
        "payload": message
    }

    try:
        response = requests.post(DEEPPAVLOV_API_URL, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request to DeepPavlov failed: {e}")
        raise

    return response.json().get('response')

def send_message_to_chatwoot(conversation_id, message_content):
    url = f"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}/messages"
    headers = {"Content-Type": "application/json", "api_access_token": CHATWOOT_ACCESS_TOKEN}
    data = {"content": message_content, "private": False}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request to Chatwoot failed: {e}")
        raise

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)))  # Enable HTTPS
