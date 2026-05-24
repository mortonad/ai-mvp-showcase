"""
MVP-F: Meeting AI Engine - Main Application
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Meeting AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Meeting AI Engine API"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Upload audio file for processing"""
    return {"message": f"File {file.filename} uploaded successfully"}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get task processing status"""
    return {"task_id": task_id, "status": "completed"}

@app.get("/summary/{task_id}")
async def get_summary(task_id: str):
    """Get meeting summary"""
    return {
        "task_id": task_id,
        "summary": "會議摘要：Q3 財務預算討論，決定增加研發投入 20%"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
