# 📚 MVP-B：多產業 RAG 知識庫平台

> **Showcase 定位**：展示 RAG (Retrieval-Augmented Generation) 架構在多產業場景的落地能力。

## 📌 核心功能

- **一鍵切換知識庫**：支援金融 (Finance)、醫療 (Medical)、法務 (Legal) 三大產業
- **TF-IDF 向量搜尋**：零外部依賴的輕量級向量檢索引擎，展示 RAG 核心概念
- **完整 RAG Pipeline**：Retrieval → Augmentation → Generation 三步驟清晰可見
- **可擴充架構**：與 LangChain + Chroma / FAISS 完全相容，可無縫升級

## 🛠️ 技術棧

| 層級 | 技術 |
|------|------|
| API 框架 | FastAPI |
| 向量搜尋 | TF-IDF (內建) / Chroma (進階) |
| RAG 架構 | LangChain RetrievalQA (可選) |
| Embedding | 內建 TF-IDF / OpenAI Embeddings (可選) |
| 容器化 | Docker + Docker Compose |

## 🚀 快速啟動

### 方式一：Docker（推薦）
```bash
docker-compose up --build
```
→ API: http://localhost:8000

### 方式二：本地執行
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API 使用範例
```bash
# 查詢金融知識庫
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"industry": "finance", "query": "投資組合最佳化的方法有哪些？"}'

# 查看支援的產業
curl http://localhost:8000/industries
```

## 📂 專案結構
```
Showcase_MVP_B_MultiRAG/
├── app/
│   ├── main.py             # FastAPI 入口
│   ├── api/
│   │   └── endpoints.py    # REST API 端點
│   └── core/
│       └── rag_engine.py   # RAG 引擎（含內建知識庫）
├── data/                   # 外部知識庫文件（可擴充）
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── MVP-B_多產業RAG知識庫平台.ipynb
└── MVP-B_資料流架構圖.md
```

## 📊 內建知識庫

| 產業 | 文件數 | 涵蓋主題 |
|------|:------:|---------|
| Finance | 3 | 投資組合理論、Black-Scholes、籌碼分析 |
| Medical | 3 | 長照指南、AI 醫療影像、牙科 AI |
| Legal | 3 | 民法條文、契約審查、個資法 |

## 🎓 對應認證
- ✅ Generative AI Applications with RAG and LangChain
- ✅ AI for Healthcare
- ✅ AI for Legal Professionals
- ✅ Deep Learning with PyTorch

## 🎯 目標職缺
- 未來巢科技 — AI 軟體工程師（匹配度 85%）
- 智信創新 — AI Engineer（匹配度 75%）
- 卡米爾 — AI 工程師（匹配度 92%）

---
*開發者：Morton Lin | 2026-05*
