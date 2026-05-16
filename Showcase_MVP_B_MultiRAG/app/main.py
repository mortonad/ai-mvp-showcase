from fastapi import FastAPI, HTTPException, UploadFile, File
from app.api import endpoints

app = FastAPI(
    title="Multi-Industry RAG Platform",
    description="A multi-industry RAG platform showcasing AI capabilities in Finance, Medical, and Legal sectors.",
    version="1.0.0"
)

app.include_router(endpoints.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Industry RAG Platform API"}
