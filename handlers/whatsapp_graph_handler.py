import os
import requests


def send_whatsapp_message(to: str, message: str):
    """Send a WhatsApp message using Meta's Graph API."""
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    token = os.getenv("WHATSAPP_TOKEN")

    if not phone_number_id or not token:
        print("❌ Missing WhatsApp API credentials")
        return {"error": "Missing credentials"}

    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ WhatsApp-besked sendt:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Fejl ved afsendelse:", e)
        return {"error": str(e)}
