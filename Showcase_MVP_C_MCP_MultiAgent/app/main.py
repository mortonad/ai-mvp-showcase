from fastapi import FastAPI
from app.core.workflow import run_multi_agent_workflow

app = FastAPI(title="MCP Multi-Agent Orchestrator")

@app.post("/run-research")
async def research(query: str):
    # 啟動 LangGraph 多代理人工作流
    result = run_multi_agent_workflow(query)
    return {"status": "completed", "result": result}

@app.get("/")
async def root():
    return {"message": "MCP Multi-Agent API is running."}
