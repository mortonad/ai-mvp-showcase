from fastapi import APIRouter, Request
from app.core.marketing_logic import handle_social_event

router = APIRouter()

@router.post("/webhook")
async def receive_event(request: Request):
    data = await request.json()
    # 這裡將事件丟給核心邏輯處理
    result = handle_social_event(data)
    return {"status": "success", "processed_result": result}
