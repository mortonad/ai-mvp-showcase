# 🤖 AI MVP Showcase Portfolio

> **專案定位**：這是我在過去 730 天中，針對不同產業痛點開發的 5 個 AI 核心原型 (PoC)。
> 
> 展示 **Agentic AI**、**Multi-RAG**、**MCP 協議**與**非同步推論**等前沿技術的落地實踐。

---

## 🚀 快速導覽 (一鍵啟動)

點擊下方的 **"Open In Colab"** 按鈕，即可在瀏覽器中直接執行各專案的核心邏輯。

| 專案名稱 | 核心技術 | 解決的問題 | 互動 Demo |
| :--- | :--- | :--- | :--- |
| **🏛️ GovAgent** | LangChain ReAct | 政府標案法規自動化評核 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mortonad/ai-mvp-showcase/blob/main/Showcase_MVP_A_GovAgent/MVP-A_政府AI_Agent教學展示.ipynb) |
| **📚 MultiRAG** | ChromaDB + RAG | 金融/醫療/法務跨領域檢索 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mortonad/ai-mvp-showcase/blob/main/Showcase_MVP_B_MultiRAG/MVP-B_多產業RAG知識庫平台.ipynb) |
| **🤖 MCP Agent** | LangGraph + MCP | 多 Agent 協作與工具調用規範 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mortonad/ai-mvp-showcase/blob/main/Showcase_MVP_C_MCP_MultiAgent/MVP-C_MCP_MultiAgent核心概念.ipynb) |
| **🎯 MarketingBot** | Prompt Eng. | 社群媒體文案自動化與排程 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mortonad/ai-mvp-showcase/blob/main/Showcase_MVP_D_MarketingBot/MVP-D_社群行銷自動化Bot.ipynb) |
| **⚡ AsyncInfer** | AsyncIO + Queue | 高併發環境下的模型推論優化 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mortonad/ai-mvp-showcase/blob/main/Showcase_MVP_E_AsyncInference/MVP-E_非同步推論排程器.ipynb) |

---

## 🏛️ MVP-A：政府 AI Agent
展示 Agentic AI 在複雜法規環境下的推理與決策能力。

```mermaid
graph TD
    A[使用者輸入文件] --> B{AI Agent 推理}
    B --> C[Thought: 分析法規需求]
    C --> D[Action: 檢索標案/採購法知識庫]
    D --> E[Observation: 發現預算編列風險]
    E --> F[產出: 結構化風險評估報告]
```

## 📚 MVP-B：多產業 RAG 平台
解決單一 LLM 無法應對專業垂直領域（醫療、金融）知識更新的問題。

```mermaid
graph LR
    A[使用者提問] --> B{路由判定}
    B -- 金融 --> C[0050 向量庫]
    B -- 醫療 --> D[長照 2.0 向量庫]
    B -- 法務 --> E[採購法向量庫]
    C & D & E --> F[RAG 增強生成回答]
```

## 🤖 MVP-C：MCP Multi-Agent 協作平台
展示基於 LangGraph 的多 Agent 協作與狀態管理能力。

```mermaid
graph LR
    User[使用者] --> Orchestrator[協作編排器]
    Orchestrator --> Agent1[搜索 Agent]
    Orchestrator --> Agent2[分析 Agent]
    Orchestrator --> Agent3[寫作 Agent]
    Agent1 & Agent2 & Agent3 --> Orchestrator
    Orchestrator --> Output[最終回覆]
```

## 🎯 MVP-D：社群行銷自動化 Bot
展示如何利用 Prompt Engineering 將品牌風格穩定地轉化為多平台的社群內容。

```mermaid
graph TD
    Raw[原始題材] --> Style[品牌風格定義]
    Style --> LLM[AI 文案生成]
    LLM --> Format[社群媒體格式轉換]
    Format --> Scheduler[自動化排程發布]
```

## ⚡ MVP-E：非同步推論排程器
針對企業級高併發場景，優化模型推論的吞吐量與穩定性。

```mermaid
graph LR
    Req[多個併發請求] --> Queue[非同步任務隊列]
    Queue --> Batch[批次處理單元]
    Batch --> Model[AI 模型推論]
    Model --> Res[回傳結果]
```

---

## 🛠️ 執行與部署 (Technical Setup)

本倉庫所有 MVP 均支援：
- **Docker 化部署**：每個資料夾內含 `Dockerfile` 與 `docker-compose.yml`。
- **Gradio 互動介面**：執行 `python app.py` 即可開啟 UI。
- **FastAPI 整合**：提供生產環境級別的 API 端點。

---
*Developed by Morton Lin | Morton 的 AI 特助系統代行*
