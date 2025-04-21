from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    # รับข้อมูลจาก Webhook
    body = await request.json()

    # แสดงข้อมูลที่ได้รับ
    print(json.dumps(body, indent=4))

    # ส่งกลับการตอบรับ
    return {"status": "success", "message": "Webhook ได้รับข้อมูลแล้ว"}
