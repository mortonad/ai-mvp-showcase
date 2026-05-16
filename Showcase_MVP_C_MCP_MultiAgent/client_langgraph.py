from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage

# 定義 Agent 的狀態
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "The messages in the conversation"]

# 初始化模型
model = ChatOpenAI(model="gpt-4-turbo-preview")

def research_agent(state: AgentState):
    """負責研究資料的代理人"""
    # 這裡未來會透過 MCP 調用工具
    return {"messages": [HumanMessage(content="[Research] 已完成客戶背景調查。")]}

def writer_agent(state: AgentState):
    """負責撰寫報告的代理人"""
    return {"messages": [HumanMessage(content="[Writer] 已根據研究結果撰寫完畢。")]}

# 建立工作流圖
workflow = StateGraph(AgentState)

# 加入節點
workflow.add_node("researcher", research_agent)
workflow.add_node("writer", writer_agent)

# 設定路徑
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

# 編譯
app = workflow.compile()

print("LangGraph Multi-Agent 工作流編譯完成。")
