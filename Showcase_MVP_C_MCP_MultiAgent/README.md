# 🤖 MVP-C：MCP Multi-Agent 協作平台

> **Showcase 定位**：展示 MCP 協議 × LangGraph Multi-Agent 的協作架構能力。

## 📌 核心功能

- **四階段 Agent Pipeline**：Researcher → Analyzer → Writer → Reviewer
- **LangGraph StateGraph**：使用 TypedDict 狀態管理與條件路由
- **MCP 協議模擬**：展示 Tool Calling 與外部資料源串接
- **品質門檻機制**：Reviewer Agent 自動評估報告品質

## 🛠️ 技術棧

| 層級 | 技術 |
|------|------|
| Agent 框架 | LangGraph (StateGraph) |
| API 框架 | FastAPI |
| MCP 協議 | MCP Server/Client (模擬) |
| 狀態管理 | TypedDict + 條件路由 |
| 容器化 | Docker + Docker Compose |

## 🚀 快速啟動

### 方式一：Docker
```bash
docker-compose up --build
```

### 方式二：本地執行
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API 使用範例
```bash
curl -X POST "http://localhost:8000/run-research?query=AI在醫療產業的應用趨勢"
```

## 📂 專案結構
```
Showcase_MVP_C_MCP_MultiAgent/
├── app/
│   ├── main.py             # FastAPI 入口
│   └── core/
│       └── workflow.py     # LangGraph 多代理人工作流
├── server.py               # MCP Server 範例
├── client_langgraph.py     # LangGraph Client 範例
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── MVP-C_MCP_MultiAgent核心概念.ipynb
```

## 🎓 對應認證
- ✅ Model Context Protocol for Leaders - Generative AI Agents
- ✅ AI Agents and Agentic AI with Python & Generative AI
- ✅ Generative AI Applications with RAG and LangChain

## 🎯 目標職缺
- 智信創新 — AI Engineer / AI 應用工程師（匹配度 75%）
- 卡米爾 — AI 工程師（匹配度 92%）
- 未來巢科技 — AI 軟體工程師（匹配度 85%）

---
*開發者：Morton Lin | 2026-05*
