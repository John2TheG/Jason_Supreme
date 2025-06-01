from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
import os
from gpt_handler import ask_jason
from handlers.ultramsg_handler import send_whatsapp_message

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / "config" / ".env")
print(f"🔑 OPENAI_API_KEY loaded? {os.getenv('OPENAI_API_KEY') is not None}")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    print("RAW incoming:", data)

    msg = data.get("data", {}).get("body")
    sender = data.get("data", {}).get("from")

    if not msg or not sender:
        print("❌ Mangler 'body' eller 'from'")
        return jsonify({"error": "Invalid message format", "received": data}), 400

    jason_reply = ask_jason(msg)
    send_whatsapp_message(sender, jason_reply)
    return jsonify({"status": "success", "message": jason_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
