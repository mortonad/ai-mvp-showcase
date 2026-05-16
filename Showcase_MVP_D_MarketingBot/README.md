# 📣 MVP-D：AI 社群行銷自動化 Bot

> **Showcase 定位**：展示 AI 驅動的社群行銷自動化能力，涵蓋文案生成、情緒分析、事件路由。

## 📌 核心功能

- **多平台文案生成**：Threads / Instagram / Facebook / LINE 各平台風格自適應
- **智能事件路由**：自動分類社群事件（留言/提及/評論/排程/諮詢）
- **情緒分析**：即時分析使用者情緒，動態調整回覆語氣
- **Lead 捕獲**：自動識別潛在客戶詢問，標記高優先級
- **多產業模板**：牙醫 / 科技 / 教育等產業專屬文案模板

## 🛠️ 技術棧

| 層級 | 技術 |
|------|------|
| API 框架 | FastAPI (Webhook) |
| NLP | 情緒分析 + 意圖分類 |
| 文案引擎 | 多平台模板 + AI 生成 |
| 容器化 | Docker + Docker Compose |

## 🚀 快速啟動

### Docker
```bash
docker-compose up --build
```

### 本地執行
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Webhook 測試
```bash
# 自動回覆
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"type": "message", "platform": "threads", "message": "你們的服務太棒了！"}'

# 文案生成
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"type": "schedule", "platform": "instagram", "industry": "dental", "topic": "牙齒美白"}'
```

## 📂 專案結構
```
Showcase_MVP_D_MarketingBot/
├── app/
│   ├── main.py             # FastAPI 入口
│   ├── api/
│   │   └── webhook.py      # Webhook 端點
│   └── core/
│       └── marketing_logic.py  # 行銷自動化核心
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── MVP-D_社群行銷自動化Bot.ipynb
```

## 🎓 對應認證
- ✅ AI-Powered Content Creation for Social Media
- ✅ Google Ads for Beginners
- ✅ GenAI for Executives & Business Leaders

## 🎯 目標職缺
- 捷德爾 — AI 應用工程師（匹配度 72%）
- 安布思沛 — Specialist Opt.（匹配度 55%）
- 卡米爾 — AI 專案經理（匹配度 92%）

---
*開發者：Morton Lin | 2026-05*
