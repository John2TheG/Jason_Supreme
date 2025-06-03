from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

app = Flask(__name__)  # Skal op før Blueprint

# ➕ Tilføj root-mappen til importstien
sys.path.append(str(Path(__file__).resolve().parent.parent))

from server.webhook import webhook  # indeholder GET /webhook (verify)
from core.gpt_handler import ask_jason
from handlers.whatsapp_graph_handler import send_whatsapp_message

# Registrér GET /webhook route
app.register_blueprint(webhook)

# 🔐 Load env-vars
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "config" / ".env")
print(f"🔑 OPENAI_API_KEY loaded? {os.getenv('OPENAI_API_KEY') is not None}")

# POST /webhook – beskedmodtagelse
@app.route('/webhook', methods=['POST'])
def webhook_post():
    data = request.get_json(force=True)
    print("RAW incoming:", data)

    msg = data.get("data", {}).get("body")
    sender = data.get("data", {}).get("from")
    from_me = data.get("data", {}).get("fromMe", False)

    if from_me:
        print("⚠️ Ignorerer besked fra botten selv")
        return jsonify({"status": "ignored own message"})

    if not msg or not sender:
        print("❌ Mangler 'body' eller 'from'")
        return jsonify({"error": "Invalid message format", "received": data}), 400

    jason_reply = ask_jason(msg)
    send_whatsapp_message(sender, jason_reply)
    return jsonify({"status": "success", "message": jason_reply})

# GET / – health check
@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "ok", "message": "Jason Supreme is running"}), 200

# 🔥 Run local server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

