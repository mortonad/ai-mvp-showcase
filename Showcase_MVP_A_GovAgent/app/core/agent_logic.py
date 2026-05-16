"""
政府 AI Agent 核心邏輯模組
- 模擬 Agentic AI 的 ReAct 推理流程
- 展示 Prompt Engineering + Tool Calling 架構
- 可替換為真實 LLM API（Gemini / OpenAI）
"""
import re
import json
from datetime import datetime


# ── 模擬知識庫（未來可接 RAG 向量搜尋） ─────────────────
GOV_KNOWLEDGE_BASE = {
    "預算編列": {
        "法規": "依《政府採購法》第 27 條，預算金額需明確列出分項說明。",
        "建議": "建議將各項目拆分至單項 50 萬元以下，以適用小額採購程序。",
    },
    "資安合規": {
        "法規": "依《資通安全管理法》第 18 條，系統需通過 A 級資安檢測。",
        "建議": "建議導入 PII 攔截機制，確保個資在傳輸與儲存階段均受保護。",
    },
    "標案撰寫": {
        "法規": "依《政府採購法》第 34 條，需備妥招標文件（含規格書、契約草案）。",
        "建議": "建議使用結構化模板：(1) 案由 (2) 需求規格 (3) 驗收標準 (4) 預算明細。",
    },
    "AI 導入": {
        "法規": "依數位發展部《行政機關使用生成式AI參考指引》。",
        "建議": "建議分階段導入：Phase 1 — 文書自動化，Phase 2 — 知識管理，Phase 3 — 決策輔助。",
    },
}


def _detect_topics(text: str) -> list[str]:
    """從文件內容中偵測涉及的主題"""
    keywords_map = {
        "預算編列": ["預算", "經費", "金額", "採購", "報價"],
        "資安合規": ["資安", "個資", "隱私", "PII", "加密", "資通安全"],
        "標案撰寫": ["標案", "招標", "投標", "服務建議書", "RFP", "驗收"],
        "AI 導入": ["AI", "人工智慧", "機器人", "自動化", "LLM", "生成式"],
    }
    detected = []
    for topic, keywords in keywords_map.items():
        if any(kw in text for kw in keywords):
            detected.append(topic)
    return detected if detected else ["標案撰寫"]  # 預設


def _simulate_react_steps(topics: list[str], user_intent: str) -> list[dict]:
    """模擬 ReAct Agent 的推理步驟（Thought → Action → Observation）"""
    steps = []
    for topic in topics:
        knowledge = GOV_KNOWLEDGE_BASE.get(topic, {})
        steps.append({
            "step_type": "Thought",
            "content": f"使用者意圖為「{user_intent}」，文件涉及「{topic}」領域，需查詢對應法規與最佳實踐。",
        })
        steps.append({
            "step_type": "Action",
            "tool": "KnowledgeBase.search",
            "query": topic,
        })
        steps.append({
            "step_type": "Observation",
            "content": f"法規依據：{knowledge.get('法規', 'N/A')}",
        })
    return steps


def process_gov_doc(doc_text: str, user_intent: str) -> dict:
    """
    處理政府文件的主函式
    
    Args:
        doc_text: 標案/公文文件內容
        user_intent: 使用者意圖（如：撰寫投標書、審查預算、合規檢查）
    
    Returns:
        dict: 包含 ReAct 推理步驟、分析結果與建議的完整回應
    """
    # Step 1: 主題偵測
    topics = _detect_topics(doc_text)
    
    # Step 2: ReAct 推理流程
    reasoning_steps = _simulate_react_steps(topics, user_intent)
    
    # Step 3: 彙整分析結果
    recommendations = []
    for topic in topics:
        knowledge = GOV_KNOWLEDGE_BASE.get(topic, {})
        recommendations.append({
            "領域": topic,
            "法規依據": knowledge.get("法規", "暫無對應法規"),
            "具體建議": knowledge.get("建議", "建議進一步諮詢主管機關"),
        })
    
    # Step 4: 風險評估
    risk_items = []
    if "預算" not in doc_text and "預算編列" in topics:
        risk_items.append("⚠️ 文件中未發現預算明細，建議補充。")
    if any(kw in doc_text for kw in ["個資", "姓名", "身分證"]):
        risk_items.append("⚠️ 文件可能包含個人資料，建議啟用 PII 攔截。")
    if len(doc_text) < 50:
        risk_items.append("⚠️ 文件內容過短，分析結果可能不完整。")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "user_intent": user_intent,
        "detected_topics": topics,
        "reasoning_trace": reasoning_steps,
        "recommendations": recommendations,
        "risk_alerts": risk_items if risk_items else ["✅ 未偵測到明顯風險"],
        "summary": (
            f"已針對文件進行 {len(topics)} 個領域的交叉分析。"
            f"涵蓋：{'、'.join(topics)}。"
            f"共產出 {len(recommendations)} 項建議與 {len(risk_items)} 項風險提醒。"
        ),
    }


# ── 新增：Gradio 用的格式化輸出 ────────────────────────
def process_gov_doc_formatted(doc_text: str, user_intent: str) -> str:
    """Gradio 介面用的格式化文字輸出"""
    result = process_gov_doc(doc_text, user_intent)
    
    output_lines = [
        f"🏛️ 政府 AI Agent 分析報告",
        f"⏰ {result['timestamp']}",
        f"🎯 使用者意圖：{result['user_intent']}",
        f"📋 偵測主題：{'、'.join(result['detected_topics'])}",
        "",
        "━━━ ReAct 推理過程 ━━━",
    ]
    
    for step in result["reasoning_trace"]:
        if step["step_type"] == "Thought":
            output_lines.append(f"💭 Thought: {step['content']}")
        elif step["step_type"] == "Action":
            output_lines.append(f"🔧 Action: {step['tool']}({step['query']})")
        elif step["step_type"] == "Observation":
            output_lines.append(f"👁️ Observation: {step['content']}")
        output_lines.append("")
    
    output_lines.append("━━━ 分析建議 ━━━")
    for rec in result["recommendations"]:
        output_lines.append(f"📌 【{rec['領域']}】")
        output_lines.append(f"   法規：{rec['法規依據']}")
        output_lines.append(f"   建議：{rec['具體建議']}")
        output_lines.append("")
    
    output_lines.append("━━━ 風險提醒 ━━━")
    for alert in result["risk_alerts"]:
        output_lines.append(f"  {alert}")
    
    output_lines.append("")
    output_lines.append(f"📊 {result['summary']}")
    
    return "\n".join(output_lines)
