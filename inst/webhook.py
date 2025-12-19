import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN")

app = Flask(__name__)

# --- VERIFY WEBHOOK (GET) ---
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return challenge, 200

    return "Verification failed", 403


# --- RECEIVE MESSAGES (POST) ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("RAW DATA:", data)

    # Instagram DM structure
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])

            for msg in messages:
                user_id = msg["from"]["id"]
                text = msg.get("text")

                print("====== NEW MESSAGE ======")
                print("From:", user_id)
                print("Message:", text)

    return "ok", 200


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
