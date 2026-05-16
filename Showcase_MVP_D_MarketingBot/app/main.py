from fastapi import FastAPI
from app.api import webhook

app = FastAPI(title="AI Social Marketing Bot Service")

app.include_router(webhook.router)

@app.get("/")
async def root():
    return {"message": "Marketing Bot API is running. Webhook endpoint at /webhook"}
