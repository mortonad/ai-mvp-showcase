"""
政府 AI Agent 教學展示 — Gradio 獨立介面
啟動方式: python app.py
"""
import gradio as gr
from app.core.agent_logic import process_gov_doc_formatted

EXAMPLE_DOC = """
本案為「智慧政府便民服務平台」建置計畫，預計導入 AI 自動化客服系統，
整合現有的民眾陳情管道，並提供 24/7 不間斷的諮詢服務。
預算總額為新臺幣 980 萬元整，包含硬體建置、軟體開發及資安檢測費用。
系統需符合《資通安全管理法》相關規定，並確保民眾個資之安全保護。
"""

with gr.Blocks(
    title="🏛️ 政府 AI Agent 教學展示",
    theme=gr.themes.Soft(primary_hue="blue"),
) as demo:
    gr.Markdown("# 🏛️ 政府 AI Agent 教學自動化 Demo")
    gr.Markdown(
        "> 本系統模擬 **Agentic AI（ReAct 架構）** 對政府標案文件進行自動分析。\n"
        "> 展示 **Prompt Engineering × Tool Calling × 知識庫檢索** 的完整流程。"
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            doc_input = gr.Textbox(
                label="📄 標案 / 公文內容",
                lines=8,
                placeholder="貼上標案文件、公文、或需求規格書...",
                value=EXAMPLE_DOC.strip(),
            )
            intent_input = gr.Textbox(
                label="🎯 您的意圖",
                placeholder="例如：審查預算合規性 / 撰寫投標書 / 評估 AI 導入可行性",
                value="審查此標案的預算合規性與資安風險",
            )
            submit_btn = gr.Button("🚀 開始 Agent 分析", variant="primary")
        
        with gr.Column(scale=1):
            output = gr.Textbox(
                label="📋 Agent 分析報告",
                lines=20,
            )
    
    submit_btn.click(
        fn=process_gov_doc_formatted,
        inputs=[doc_input, intent_input],
        outputs=output,
    )
    
    gr.Markdown("---")
    gr.Markdown(
        "**技術棧**: FastAPI + Gradio + LangChain (ReAct Agent 架構)  \n"
        "**認證對應**: AI Agents and Agentic AI × AI in Government × MCP 協議  \n"
        "**開發者**: Morton Lin"
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
