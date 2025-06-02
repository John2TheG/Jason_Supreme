from flask import Blueprint, request

webhook = Blueprint('webhook', __name__)

VERIFY_TOKEN = "supreme_token_123"  # Skal matche det du skrev i Meta

@webhook.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Meta webhook verified")
        return challenge, 200
    else:
        print("❌ Webhook verification failed. Args:", request.args)
        return "Forbidden", 403
