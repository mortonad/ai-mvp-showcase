from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.rag_engine import RAGEngine

router = APIRouter()
engine = RAGEngine()

class QueryRequest(BaseModel):
    industry: str
    query: str

@router.post("/query")
async def query_rag(request: QueryRequest):
    if request.industry not in ["finance", "medical", "legal"]:
        raise HTTPException(status_code=400, detail="Invalid industry. Choose from finance, medical, legal.")
    
    try:
        response = engine.ask(request.industry, request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/industries")
async def get_industries():
    return {"industries": ["finance", "medical", "legal"]}
