import os
import requests

def send_whatsapp_message(to, message):
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    token = os.getenv("ULTRAMSG_TOKEN")

    if not instance_id or not token:
        print("❌ Mangler ULTRAMSG credentials")
        return {"error": "Missing credentials"}

    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {
        "token": token,
        "to": to,
        "body": message
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("✅ WhatsApp-besked sendt:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Fejl ved afsendelse:", e)
        return {"error": str(e)}

