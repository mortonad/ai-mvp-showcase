"""
社群行銷自動化 Bot — 核心邏輯
- 社群事件分類與路由
- AI 文案自動生成（多平台：FB / IG / Threads / LINE）
- 標籤推薦與互動策略建議
"""
import re
from datetime import datetime
from typing import Optional


# ── 平台風格模板 ─────────────────────────────────────
PLATFORM_STYLES = {
    "threads": {
        "max_length": 500,
        "tone": "輕鬆對話、有個性",
        "emoji_density": "高",
        "hashtag_count": 3,
    },
    "instagram": {
        "max_length": 2200,
        "tone": "視覺導向、故事感",
        "emoji_density": "中",
        "hashtag_count": 15,
    },
    "facebook": {
        "max_length": 5000,
        "tone": "專業但親切",
        "emoji_density": "低",
        "hashtag_count": 5,
    },
    "line": {
        "max_length": 500,
        "tone": "簡潔直接、行動呼籲明確",
        "emoji_density": "中",
        "hashtag_count": 0,
    },
}


# ── 產業文案模板 ─────────────────────────────────────
INDUSTRY_TEMPLATES = {
    "dental": {
        "greeting": "😁 您的牙齒健康，是我們最大的關注！",
        "cta": "📞 立即預約免費諮詢 → {link}",
        "topics": ["洗牙保健", "牙齒美白", "植牙諮詢", "兒童牙科"],
    },
    "tech": {
        "greeting": "🚀 AI 時代，你準備好了嗎？",
        "cta": "👉 了解更多 AI 解決方案 → {link}",
        "topics": ["AI 自動化", "數據分析", "智慧客服", "流程優化"],
    },
    "education": {
        "greeting": "📚 學習，從不嫌晚！",
        "cta": "🎓 免費試聽課程 → {link}",
        "topics": ["AI 課程", "技能提升", "職涯轉換", "實戰工作坊"],
    },
}


def classify_event(event_data: dict) -> dict:
    """
    分類社群事件類型
    
    支援事件類型:
    - message: 使用者留言 → 自動回覆
    - mention: 被提及 → 互動回應  
    - comment: 評論 → 情緒分析 + 回覆
    - schedule: 排程發文 → 文案生成
    """
    event_type = event_data.get("type", "message")
    platform = event_data.get("platform", "threads")
    
    classifications = {
        "message": {"action": "auto_reply", "priority": "high"},
        "mention": {"action": "engage", "priority": "medium"},
        "comment": {"action": "sentiment_reply", "priority": "medium"},
        "schedule": {"action": "generate_content", "priority": "low"},
        "inquiry": {"action": "lead_capture", "priority": "high"},
    }
    
    result = classifications.get(event_type, {"action": "auto_reply", "priority": "low"})
    result["event_type"] = event_type
    result["platform"] = platform
    
    return result


def analyze_sentiment(text: str) -> dict:
    """簡易情緒分析（模擬）"""
    positive_words = ["讚", "好", "棒", "推", "喜歡", "感謝", "謝謝", "太好了", "優秀", "amazing", "great", "love"]
    negative_words = ["差", "爛", "糟", "貴", "慢", "不好", "失望", "bad", "terrible", "horrible"]
    
    text_lower = text.lower()
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    if pos_count > neg_count:
        return {"sentiment": "positive", "score": 0.8, "emoji": "😊"}
    elif neg_count > pos_count:
        return {"sentiment": "negative", "score": 0.3, "emoji": "😟"}
    else:
        return {"sentiment": "neutral", "score": 0.5, "emoji": "😐"}


def generate_auto_reply(message: str, platform: str = "threads") -> str:
    """根據平台風格生成自動回覆"""
    sentiment = analyze_sentiment(message)
    style = PLATFORM_STYLES.get(platform, PLATFORM_STYLES["threads"])
    
    if sentiment["sentiment"] == "positive":
        reply = f"感謝您的回饋！{sentiment['emoji']} 您的支持是我們最大的動力！"
    elif sentiment["sentiment"] == "negative":
        reply = f"非常抱歉造成您的不便 {sentiment['emoji']} 我們會立即改善，請私訊告訴我們更多細節，讓我們為您處理 🙏"
    else:
        reply = f"感謝您的訊息！{sentiment['emoji']} 有任何問題歡迎隨時詢問，我們很樂意為您服務！"
    
    return reply


def generate_marketing_content(
    topic: str,
    platform: str = "threads",
    industry: str = "tech",
    link: str = "https://example.com",
) -> dict:
    """
    AI 驅動的行銷文案生成
    
    Args:
        topic: 文案主題
        platform: 目標平台
        industry: 產業類別
        link: CTA 連結
    
    Returns:
        dict: 包含文案、標籤、發佈建議的完整結果
    """
    style = PLATFORM_STYLES.get(platform, PLATFORM_STYLES["threads"])
    template = INDUSTRY_TEMPLATES.get(industry, INDUSTRY_TEMPLATES["tech"])
    
    # 生成主文案
    content_parts = [
        template["greeting"],
        "",
        f"今天來聊聊 #{topic} 🔥",
        "",
    ]
    
    if platform == "threads":
        content_parts.extend([
            f"你知道嗎？{topic}正在改變整個產業的遊戲規則。",
            f"我們最近發現了 3 個關鍵趨勢，讓我分享給你 👇",
            "",
            f"1️⃣ 自動化程度大幅提升",
            f"2️⃣ 客製化體驗成為標配",
            f"3️⃣ 數據驅動決策不再是選項，而是必備",
            "",
        ])
    elif platform == "instagram":
        content_parts.extend([
            f"✨ {topic}的 3 大趨勢，你跟上了嗎？",
            "",
            f"📌 趨勢一：自動化已成為基本功",
            f"📌 趨勢二：個人化體驗是新標準",
            f"📌 趨勢三：AI 輔助決策不再遙遠",
            "",
            f"💡 關注我們，掌握最新動態！",
            "",
        ])
    else:
        content_parts.extend([
            f"【{topic}深度分析】",
            "",
            f"隨著 AI 技術的快速發展，{topic}正面臨前所未有的變革。",
            f"我們整理了最新的產業趨勢與實戰策略，幫助您在競爭中脫穎而出。",
            "",
        ])
    
    content_parts.append(template["cta"].format(link=link))
    
    # 生成標籤
    hashtags = [
        f"#{topic.replace(' ', '')}",
        "#AI自動化",
        "#數位轉型",
    ]
    if industry == "dental":
        hashtags.extend(["#牙醫", "#口腔健康"])
    elif industry == "education":
        hashtags.extend(["#學習", "#技能提升"])
    
    hashtags = hashtags[:style["hashtag_count"]] if style["hashtag_count"] > 0 else []
    
    if hashtags:
        content_parts.append("")
        content_parts.append(" ".join(hashtags))
    
    full_content = "\n".join(content_parts)
    
    return {
        "content": full_content[:style["max_length"]],
        "platform": platform,
        "industry": industry,
        "hashtags": hashtags,
        "character_count": len(full_content),
        "sentiment_tone": style["tone"],
        "best_posting_time": "週二/四 12:00-13:00 或 20:00-21:00",
        "engagement_tips": [
            "發文後 30 分鐘內回覆所有留言",
            "使用問句結尾增加互動率",
            "搭配圖片/影片提升觸及率 2-3 倍",
        ],
    }


def handle_social_event(event_data: dict) -> dict:
    """
    社群事件處理主函式
    
    Args:
        event_data: {
            "type": "message" | "comment" | "mention" | "schedule" | "inquiry",
            "platform": "threads" | "instagram" | "facebook" | "line",
            "message": "使用者訊息內容",
            "industry": "dental" | "tech" | "education",
            "topic": "文案主題（用於 schedule 類型）",
        }
    
    Returns:
        dict: 處理結果
    """
    # Step 1: 事件分類
    classification = classify_event(event_data)
    
    message = event_data.get("message", "")
    platform = event_data.get("platform", "threads")
    industry = event_data.get("industry", "tech")
    
    # Step 2: 根據分類執行對應動作
    if classification["action"] == "auto_reply":
        reply = generate_auto_reply(message, platform)
        sentiment = analyze_sentiment(message)
        return {
            "action": "auto_reply",
            "reply": reply,
            "sentiment": sentiment,
            "classification": classification,
            "timestamp": datetime.now().isoformat(),
        }
    
    elif classification["action"] == "generate_content":
        topic = event_data.get("topic", "AI 應用趨勢")
        content = generate_marketing_content(topic, platform, industry)
        return {
            "action": "generate_content",
            "generated": content,
            "classification": classification,
            "timestamp": datetime.now().isoformat(),
        }
    
    elif classification["action"] == "sentiment_reply":
        sentiment = analyze_sentiment(message)
        reply = generate_auto_reply(message, platform)
        return {
            "action": "sentiment_reply",
            "reply": reply,
            "sentiment": sentiment,
            "classification": classification,
            "timestamp": datetime.now().isoformat(),
        }
    
    elif classification["action"] == "lead_capture":
        return {
            "action": "lead_capture",
            "reply": "感謝您的詢問！我們的專人會盡快與您聯繫 📞",
            "lead_info": {
                "source": platform,
                "message": message,
                "priority": "high",
            },
            "classification": classification,
            "timestamp": datetime.now().isoformat(),
        }
    
    else:
        reply = generate_auto_reply(message, platform)
        return {
            "action": "engage",
            "reply": reply,
            "classification": classification,
            "timestamp": datetime.now().isoformat(),
        }
