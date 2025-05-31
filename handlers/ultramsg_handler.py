import os
import requests

def send_whatsapp_message(to, message):
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    token = os.getenv("ULTRAMSG_TOKEN")
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {
        "token": token,
        "to": to,
        "body": message
    }
    response = requests.post(url, data=payload)
    return response.json()
