# 💬 MVP-F：會議 AI 引擎

> **Showcase 定位**：展示語音轉文字（STT）+ AI 會議摘要 + LINE Bot 整合的完整解決方案。

## 📌 核心功能

- **語音轉文字**：GCP STT API 支援多語音格式
- **AI 會議摘要**：自動提取會議重點、行動項目、決策記錄
- **LINE Bot 整合**：即時會議通知、摘要分享
- **雙生態系整合**：Google Apps Script + Microsoft Graph API

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
# 上傳音頻文件
curl -X POST http://localhost:8000/upload \
  -F "audio=@meeting.mp3"

# 查詢處理狀態
curl http://localhost:8000/tasks/{task_id}

# 獲取會議摘要
curl http://localhost:8000/summary/{task_id}
```

## 🎓 對應認證
- ✅ Deep Learning with PyTorch
- ✅ Machine Learning with Python

## 🎯 目標職缺
- 三弦科技 — 後端系統工程師（匹配度 65%）
- 摘星數據 — 軟體開發工程師（匹配度 70%）

---
*開發者：Morton Lin | 2026-05*
