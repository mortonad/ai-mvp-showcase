# 🏛️ MVP-A：政府 AI Agent 教學自動化

> **Showcase 定位**：展示 Agentic AI 在政府公部門場景的落地能力。

## 📌 核心功能

- **ReAct 推理引擎**：模擬 Thought → Action → Observation 的 Agent 推理流程
- **知識庫檢索**：涵蓋預算編列、資安合規、標案撰寫、AI 導入等領域
- **風險評估**：自動偵測文件中的潛在風險（PII 洩露、預算缺漏等）
- **結構化報告**：產出可追溯的分析報告，包含法規依據與具體建議

## 🛠️ 技術棧

| 層級 | 技術 |
|------|------|
| API 框架 | FastAPI |
| 展示介面 | Gradio (Blocks) |
| Agent 架構 | ReAct Pattern (模擬) |
| 知識管理 | 內建知識庫（可擴充 RAG） |
| 容器化 | Docker + Docker Compose |

## 🚀 快速啟動

### 方式一：Docker（推薦）
```bash
docker-compose up --build
```
→ 瀏覽 http://localhost:7860

### 方式二：本地執行
```bash
pip install -r requirements.txt
python app.py
```

### 方式三：FastAPI + Gradio 掛載
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
→ API: http://localhost:8000 | GUI: http://localhost:8000/gui

## 📂 專案結構
```
Showcase_MVP_A_GovAgent/
├── app.py                  # Gradio 獨立啟動入口
├── app/
│   ├── main.py             # FastAPI + Gradio 掛載
│   ├── api/                # REST API 端點
│   └── core/
│       └── agent_logic.py  # ReAct Agent 核心邏輯
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── MVP-A_政府AI_Agent教學展示.ipynb  # 教學 Notebook
```

## 🎓 對應認證
- ✅ AI Agents and Agentic AI with Python & Generative AI
- ✅ AI in Government
- ✅ Model Context Protocol for Leaders
- ✅ Foundations of Agile Project Management

## 🎯 目標職缺
- 卡米爾 — 政府機關駐點 AI 工程師（匹配度 95%）
- 卡米爾 — AI 工程師（匹配度 92%）
- 卡米爾 — AI 專案經理（匹配度 92%）

---
*開發者：Morton Lin | 2026-05*
