"""
MCP Multi-Agent 協作工作流
- 模擬 LangGraph StateGraph 的多代理人協作流程
- 展示 Researcher → Analyzer → Writer → Reviewer 四階段 pipeline
- 架構相容 MCP Server/Client 擴充
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict
from datetime import datetime


class AgentState(TypedDict):
    query: str
    research_data: str
    analysis: str
    report: str
    review: str
    metadata: dict


# ── Agent Node 定義 ──────────────────────────────────

def researcher_node(state: AgentState) -> dict:
    """
    研究員 Agent — 負責資料蒐集與初步整理
    模擬從 MCP Server 抓取外部資料
    """
    query = state["query"]
    
    # 模擬 MCP Tool Calling: search_industry_data
    simulated_data = {
        "AI": {
            "trends": "2026 年 Agentic AI 成為主流，MCP 協議標準化 Agent 與工具溝通",
            "market_size": "全球 AI 市場規模預估 2026 年達 $5,000 億美元",
            "key_players": "OpenAI, Google DeepMind, Anthropic, Meta AI",
        },
        "醫療": {
            "trends": "AI 輔助診斷準確率持續提升，FDA 已核准 700+ AI 醫材",
            "market_size": "數位健康市場 2026 年預估 $3,790 億美元",
            "key_players": "Google Health, NVIDIA Clara, PathAI",
        },
        "金融": {
            "trends": "AI 量化交易佔比突破 60%，RAG 技術應用於合規審查",
            "market_size": "FinTech 市場 2026 年預估 $3,320 億美元",
            "key_players": "Bloomberg GPT, Ant Group, Stripe",
        },
    }
    
    # 根據查詢內容選擇最相關的產業資料
    best_match = "AI"
    for industry in simulated_data:
        if industry in query:
            best_match = industry
            break
    
    data = simulated_data[best_match]
    research_result = (
        f"📡 [Researcher Agent] 已透過 MCP Tool 蒐集「{best_match}」產業資料：\n"
        f"  ▸ 趨勢：{data['trends']}\n"
        f"  ▸ 市場規模：{data['market_size']}\n"
        f"  ▸ 主要玩家：{data['key_players']}\n"
    )
    
    return {
        "research_data": research_result,
        "metadata": {
            "researcher_timestamp": datetime.now().isoformat(),
            "industry": best_match,
            "mcp_tools_used": ["search_industry_data", "get_market_report"],
        },
    }


def analyzer_node(state: AgentState) -> dict:
    """
    分析師 Agent — 負責資料分析與洞察提取
    """
    research = state["research_data"]
    query = state["query"]
    
    analysis = (
        f"📊 [Analyzer Agent] 基於研究資料的深度分析：\n"
        f"  ▸ 機會評估：該領域正處於高速成長期，技術成熟度提升帶動商業化加速\n"
        f"  ▸ 風險因素：市場競爭激烈，需差異化定位\n"
        f"  ▸ 建議策略：聚焦垂直產業 AI 落地（醫療/法務/政府），\n"
        f"    利用 MCP 標準化協議降低整合成本\n"
        f"  ▸ ROI 預估：導入 AI 可提升作業效率 40-60%\n"
    )
    
    return {"analysis": analysis}


def writer_node(state: AgentState) -> dict:
    """
    撰稿人 Agent — 負責將分析結果整合為結構化報告
    """
    report = (
        f"📝 [Writer Agent] 產業 AI 應用研究報告\n"
        f"{'='*50}\n\n"
        f"一、研究摘要\n{state['research_data']}\n\n"
        f"二、分析洞察\n{state['analysis']}\n\n"
        f"三、行動建議\n"
        f"  1. 短期（1-3 月）：完成 MVP 開發，驗證核心技術可行性\n"
        f"  2. 中期（3-6 月）：與目標客戶進行 PoC 合作\n"
        f"  3. 長期（6-12 月）：標準化為 SaaS 產品，建立銷售管道\n\n"
        f"四、附錄\n"
        f"  - 查詢主題：{state['query']}\n"
        f"  - Agent 協作流程：Researcher → Analyzer → Writer → Reviewer\n"
        f"  - MCP 工具呼叫次數：2\n"
    )
    
    return {"report": report}


def reviewer_node(state: AgentState) -> dict:
    """
    審閱者 Agent — 負責品質檢查與最終驗證
    """
    review = (
        f"✅ [Reviewer Agent] 品質審查結果：\n"
        f"  ▸ 資料完整性：✅ 通過（含趨勢、市場規模、主要玩家）\n"
        f"  ▸ 分析邏輯性：✅ 通過（機會-風險-策略架構完整）\n"
        f"  ▸ 行動可行性：✅ 通過（短中長期目標明確）\n"
        f"  ▸ 總體評分：A（報告品質優良，建議直接交付）\n"
    )
    
    return {"review": review}


# ── 條件路由函式 ─────────────────────────────────────

def should_review(state: AgentState) -> str:
    """判斷報告是否需要審閱"""
    # 模擬品質門檻判斷
    if len(state.get("report", "")) > 100:
        return "reviewer"
    return "end"


# ── 主要工作流入口 ───────────────────────────────────

def run_multi_agent_workflow(query: str) -> dict:
    """
    執行完整的多代理人工作流
    
    流程: Researcher → Analyzer → Writer → Reviewer (條件路由)
    
    Args:
        query: 使用者的研究主題
    
    Returns:
        dict: 包含完整 Agent 協作結果的狀態
    """
    workflow = StateGraph(AgentState)
    
    # 註冊 Agent Nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("reviewer", reviewer_node)
    
    # 設定入口
    workflow.set_entry_point("researcher")
    
    # 設定邊（Agent 協作順序）
    workflow.add_edge("researcher", "analyzer")
    workflow.add_edge("analyzer", "writer")
    
    # 條件路由：Writer → Reviewer or End
    workflow.add_conditional_edges(
        "writer",
        should_review,
        {"reviewer": "reviewer", "end": END},
    )
    workflow.add_edge("reviewer", END)
    
    # 編譯與執行
    chain = workflow.compile()
    result = chain.invoke({
        "query": query,
        "research_data": "",
        "analysis": "",
        "report": "",
        "review": "",
        "metadata": {},
    })
    
    return result
