"""
多產業 RAG 知識庫引擎
- 支援 Finance / Medical / Legal 三大產業知識庫
- 提供 TF-IDF 向量搜尋 (零依賴模式) + 可選 LangChain + Chroma 模式
- 無需 API Key 即可展示完整 RAG 流程
"""
import os
import re
import math
from collections import Counter
from typing import Optional


# ── 內建示範知識庫 ─────────────────────────────────
DEMO_KNOWLEDGE = {
    "finance": [
        {
            "id": "FIN-001",
            "title": "投資組合最佳化理論",
            "content": "現代投資組合理論 (Modern Portfolio Theory, MPT) 由 Harry Markowitz 於 1952 年提出。核心概念為透過多元資產配置，在給定風險水準下最大化預期報酬。常用工具包括 PyPortfolioOpt、cvxpy 等。風險衡量指標：標準差、VaR (Value at Risk)、Sharpe Ratio。",
        },
        {
            "id": "FIN-002",
            "title": "Black-Scholes 選擇權定價模型",
            "content": "Black-Scholes 模型是衍生性金融商品定價的經典模型，假設標的資產價格服從幾何布朗運動。公式：C = S*N(d1) - K*e^(-rT)*N(d2)。Python 實作可使用 scipy.stats.norm 計算 N(d) 值。",
        },
        {
            "id": "FIN-003",
            "title": "股市籌碼分析方法論",
            "content": "籌碼分析聚焦於三大法人（外資、投信、自營商）的買賣超數據。關鍵指標包括：外資連續買超天數、融資融券餘額變化、大戶持股比例。技術實作：透過 TWSE API 抓取每日法人買賣超數據，結合 Pandas 進行趨勢分析。",
        },
    ],
    "medical": [
        {
            "id": "MED-001",
            "title": "長期照護指南 — 多重慢性病管理",
            "content": "依據衛福部《長期照顧服務法》，65 歲以上具多重慢性病（如：第二型糖尿病合併輕度腎功能下降）者，需制定個別化照護計畫。重點：蛋白質攝取量控制（0.6-0.8g/kg/day）、血糖監測頻率（每日 2-4 次）、運動處方（每週 150 分鐘中強度有氧運動）。",
        },
        {
            "id": "MED-002",
            "title": "AI 輔助醫療影像判讀",
            "content": "利用深度學習模型（如 ResNet、EfficientNet）進行醫療影像分析。應用場景包括：X 光片異常偵測、皮膚病灶分類、口腔疾病篩檢。關鍵技術：遷移學習 (Transfer Learning)、Grad-CAM 可解釋性、DICOM 影像處理。",
        },
        {
            "id": "MED-003",
            "title": "牙科 AI 應用趨勢",
            "content": "牙科 AI 主要應用於四大場景：(1) 口腔 X 光自動判讀 — 偵測蛀牙、牙周病、根尖病變；(2) 智能預約排程 — 根據治療類型自動分配時段；(3) 病歷知識庫 — RAG 架構輔助醫師查詢類似病例；(4) 病患溝通 — Chatbot 自動回覆常見問題。",
        },
    ],
    "legal": [
        {
            "id": "LEG-001",
            "title": "民法 第 9-1 條 — 死亡宣告規定",
            "content": "依《民法》第 9-1 條，失蹤人失蹤滿七年後，法院得因利害關係人或檢察官之聲請，為死亡之宣告。如遇特別災難，失蹤滿一年即可聲請。宣告死亡後，其財產之繼承與婚姻關係準用死亡之規定。AI 可協助自動比對法條引用與案例判決。",
        },
        {
            "id": "LEG-002",
            "title": "契約審查自動化",
            "content": "AI 契約審查的核心功能：(1) 條款風險標記 — 識別不利條款如違約金過高、管轄權約定等；(2) 法規比對 — 自動引用相關法律條文；(3) Before/After 改善建議 — 提供修改前後的對比。技術實作：Prompt Engineering + 領域知識嵌入。",
        },
        {
            "id": "LEG-003",
            "title": "個人資料保護法重點",
            "content": "《個人資料保護法》要求蒐集、處理、利用個人資料應符合特定目的，並取得當事人書面同意。違反者可處五萬至五十萬元罰鍰。AI 系統需內建 PII 攔截機制，確保姓名、身分證字號、電話等敏感資訊在處理過程中受到保護。",
        },
    ],
}


class SimpleVectorSearch:
    """
    輕量級 TF-IDF 向量搜尋（零外部依賴）
    - 不需要 OpenAI API Key
    - 展示向量搜尋的核心概念
    """

    def __init__(self, documents: list[dict]):
        self.documents = documents
        self._build_index()

    def _tokenize(self, text: str) -> list[str]:
        """簡易斷詞（中文按字切分 + 英文按空格切分）"""
        # 提取英文單詞
        english_words = re.findall(r'[a-zA-Z]+', text.lower())
        # 提取中文字
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        # 提取中文雙字詞（bigram）
        chinese_bigrams = [text[i:i+2] for i in range(len(text)-1)
                           if all('\u4e00' <= c <= '\u9fff' for c in text[i:i+2])]
        return english_words + chinese_chars + chinese_bigrams

    def _build_index(self):
        """建立 TF-IDF 索引"""
        self.doc_tokens = []
        self.df = Counter()  # Document Frequency
        
        for doc in self.documents:
            tokens = self._tokenize(doc["content"] + " " + doc["title"])
            token_set = set(tokens)
            self.doc_tokens.append(Counter(tokens))
            for token in token_set:
                self.df[token] += 1

    def search(self, query: str, top_k: int = 2) -> list[dict]:
        """搜尋最相關的文件"""
        query_tokens = self._tokenize(query)
        n_docs = len(self.documents)
        scores = []
        
        for i, doc_tf in enumerate(self.doc_tokens):
            score = 0.0
            for token in query_tokens:
                tf = doc_tf.get(token, 0)
                df = self.df.get(token, 0)
                if tf > 0 and df > 0:
                    idf = math.log(n_docs / df + 1)
                    score += tf * idf
            scores.append((score, i))
        
        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score > 0:
                doc = self.documents[idx].copy()
                doc["relevance_score"] = round(score, 2)
                results.append(doc)
        
        return results


class MultiIndustryRAG:
    """
    多產業 RAG 引擎
    - 支援一鍵切換產業知識庫
    - 內建示範資料，無需外部 API
    - 架構相容 LangChain + Chroma（進階模式）
    """

    def __init__(self):
        self.engines: dict[str, SimpleVectorSearch] = {}
        self._load_demo_data()

    def _load_demo_data(self):
        """載入內建示範知識庫"""
        for industry, docs in DEMO_KNOWLEDGE.items():
            self.engines[industry] = SimpleVectorSearch(docs)

    def get_industries(self) -> list[str]:
        return list(self.engines.keys())

    def ask(self, industry: str, query: str) -> dict:
        """
        執行 RAG 查詢
        
        Returns:
            dict: {query, industry, retrieved_docs, answer, sources}
        """
        if industry not in self.engines:
            return {
                "error": f"不支援的產業: {industry}",
                "available": self.get_industries(),
            }
        
        # Step 1: Retrieval — 從向量搜尋引擎中檢索相關文件
        retrieved = self.engines[industry].search(query, top_k=2)
        
        if not retrieved:
            return {
                "query": query,
                "industry": industry,
                "answer": "未找到相關文件，請嘗試其他關鍵字。",
                "sources": [],
            }
        
        # Step 2: Augmented Generation — 基於檢索結果生成回答
        context = "\n\n".join([
            f"【{doc['title']}】\n{doc['content']}"
            for doc in retrieved
        ])
        
        # 模擬 LLM 生成（展示架構用，可替換為真實 API）
        answer = (
            f"根據 {industry.upper()} 產業知識庫的檢索結果，"
            f"針對您的問題「{query}」，以下是整合分析：\n\n"
        )
        for doc in retrieved:
            answer += f"📌 {doc['title']}（相關度 {doc['relevance_score']}）\n"
            answer += f"   {doc['content'][:150]}...\n\n"
        
        answer += (
            "💡 以上資訊來自經過向量搜尋（TF-IDF）檢索的知識庫文件。"
            "在生產環境中，此步驟會將檢索結果送入 LLM（如 GPT-4 / Gemini）"
            "進行更精確的自然語言回答生成。"
        )
        
        return {
            "query": query,
            "industry": industry,
            "retrieved_docs": retrieved,
            "answer": answer,
            "sources": [doc["id"] for doc in retrieved],
            "rag_pipeline": {
                "retrieval_method": "TF-IDF Vector Search",
                "top_k": 2,
                "generation_model": "Simulated (replaceable with GPT-4/Gemini)",
            },
        }
