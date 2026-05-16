# ⚡ MVP-E：非同步 AI 推論排程器

> **Showcase 定位**：展示高併發非同步推論架構，含任務佇列、進度追蹤、結果取回。

## 📌 核心功能

- **任務佇列**：In-Memory Queue（生產環境可替換為 Redis + Celery）
- **進度追蹤**：5 階段進度回報（0% → 20% → 40% → 60% → 80% → 100%）
- **多任務類型**：策略回測 (backtest) + 情緒分析 (sentiment)
- **狀態機**：QUEUED → RUNNING → COMPLETED / FAILED

## 🚀 快速啟動

```bash
# Docker
docker-compose up --build

# 本地
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### API 使用
```bash
# 提交回測任務
curl -X POST http://localhost:8000/submit/backtest \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSMC"}'

# 查詢狀態
curl http://localhost:8000/tasks/{task_id}

# 列出所有任務
curl http://localhost:8000/tasks
```

## 🎓 對應認證
- ✅ Deep Learning with PyTorch
- ✅ Machine Learning with Python

## 🎯 目標職缺
- 三弦科技 — 後端系統工程師（匹配度 65%）
- 摘星數據 — 軟體開發工程師（匹配度 70%）

---
*開發者：Morton Lin | 2026-05*
