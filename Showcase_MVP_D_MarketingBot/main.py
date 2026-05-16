from fastapi import FastAPI, Request

app = FastAPI(title="AI Social Marketing Bot")

@app.post("/webhook")
async def webhook(request: Request):
    # 此處整合 Meta x Manus 行銷機器人的 Webhook 邏輯
    data = await request.json()
    return {"status": "received", "data": data}

@app.get("/health")
async def health():
    return {"status": "ok"}
