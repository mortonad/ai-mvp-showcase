import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.scheduler import task_queue, execute_task_async

app = FastAPI(title="Async AI Inference Scheduler", version="1.0.0")

class BacktestRequest(BaseModel):
    symbol: str = "TSMC"

class SentimentRequest(BaseModel):
    text: str = "AI is amazing"

@app.post("/submit/backtest")
async def submit_backtest(req: BacktestRequest):
    task_id = task_queue.submit("backtest", {"symbol": req.symbol})
    threading.Thread(target=execute_task_async, args=(task_id, "backtest", {"symbol": req.symbol})).start()
    return {"status": "accepted", "task_id": task_id, "check": f"/tasks/{task_id}"}

@app.post("/submit/sentiment")
async def submit_sentiment(req: SentimentRequest):
    task_id = task_queue.submit("sentiment", {"text": req.text})
    threading.Thread(target=execute_task_async, args=(task_id, "sentiment", {"text": req.text})).start()
    return {"status": "accepted", "task_id": task_id, "check": f"/tasks/{task_id}"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    t = task_queue.get_task(task_id)
    if not t:
        raise HTTPException(404, f"Task {task_id} not found")
    return t.to_dict()

@app.get("/tasks")
async def list_tasks(limit: int = 20):
    return {"tasks": task_queue.list_tasks(limit)}

@app.get("/")
async def root():
    return {"service": "Async AI Inference Scheduler", "endpoints": ["/submit/backtest", "/submit/sentiment", "/tasks/{id}", "/tasks"]}
