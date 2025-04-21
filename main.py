from fastapi import FastAPI, Request
import json
import requests

app = FastAPI()

# LINE API settings (ใช้ LINE Messaging API ส่งแจ้งเตือนให้แอดมิน)
LINE_ACCESS_TOKEN = '0iM/gg2Fj9sfdfw9pgEa9bSqLquHGZTgXyVub75iHO3TngYJKrMRrKy15BgCdlrAaBmicPz8c/5dkwce2ebL28zVKpV/6SSdnOnSFzX92jyakeBbPZOKjkzT8duPa8kB+km4j49TPnB5TdpDM29G7AdB04t89/1O/w1cDnyilFU='  # ใช้ Channel Access Token ของคุณ
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'  # URL สำหรับส่งข้อความ
ADMIN_USER_ID = 'U85e0052a3176ddd793470a41b02b69fe'  # ใช้ User ID ของแอดมินที่ต้องการให้แชทบอทส่งข้อความไปหา

# ฟังก์ชันส่งข้อความแจ้งเตือนให้แอดมิน
def send_line_message(user_id: str, message: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    
    data = {
        "to": user_id,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    
    response = requests.post(LINE_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Error sending message: {response.status_code}")
        print(response.text)

# รับข้อมูลจาก webhook และส่งข้อความแจ้งเตือนไปยังแอดมิน
@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    # ตรวจสอบว่ามีข้อมูลจากฟอร์มส่งมาใน webhook
    if "events" in body:
        for event in body["events"]:
            if event.get("type") == "message":
                # ข้อมูลที่ได้รับจากข้อความ
                user_id = event["source"]["userId"]
                message_text = event["message"]["text"]
                
                # ส่งข้อความแจ้งเตือนให้แอดมิน
                send_line_message(ADMIN_USER_ID, f"จาก User ID: {user_id}\nข้อความที่ส่ง: {message_text}")

    return {"status": "success", "message": "Webhook ได้รับข้อมูลแล้ว"}
