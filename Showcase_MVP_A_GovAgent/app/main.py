"""
政府 AI Agent 教學展示 — FastAPI + Gradio 掛載模式
啟動方式: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
from app.core.agent_logic import process_gov_doc, process_gov_doc_formatted

app = FastAPI(title="Gov AI Agent Platform")


# ── REST API 模型 ────────────────────────────────────
class AnalyzeRequest(BaseModel):
    doc_text: str
    user_intent: str


# ── REST API 端點（供外部整合） ──────────────────────
@app.get("/")
async def root():
    return {"message": "Gov AI Agent API is running. Access GUI at /gui"}


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    """回傳結構化 JSON 分析結果"""
    return process_gov_doc(req.doc_text, req.user_intent)


# ── Gradio 介面（使用格式化文字輸出） ────────────────
io = gr.Interface(
    fn=process_gov_doc_formatted,
    inputs=[
        gr.Textbox(label="📄 標案 / 公文內容", lines=8,
                   placeholder="貼上標案文件、公文、或需求規格書..."),
        gr.Textbox(label="🎯 您的意圖",
                   placeholder="例如：審查預算合規性 / 撰寫投標書"),
    ],
    outputs=gr.Textbox(label="📋 Agent 分析報告", lines=20,
                       show_copy_button=True),
    title="🏛️ 政府 AI Agent 教學自動化",
    theme=gr.themes.Soft(primary_hue="blue"),
)

# 將 Gradio 掛載到 FastAPI
app = gr.mount_gradio_app(app, io, path="/gui")
