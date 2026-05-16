# MVP-B 多產業 RAG 知識庫平台 - 資料流架構圖

## 系統架構圖

```mermaid
graph TB
    subgraph "資料輸入層"
        A[金融資料] --> D[文件載入器]
        B[醫療資料] --> D
        C[法務資料] --> D
    end
    
    subgraph "資料處理層"
        D --> E[文字分割器<br/>Chunk Size: 1000]
        E --> F[OpenAI Embeddings<br/>text-embedding-ada-002]
    end
    
    subgraph "向量儲存層"
        F --> G[ChromaDB<br/>金融向量庫]
        F --> H[ChromaDB<br/>醫療向量庫]
        F --> I[ChromaDB<br/>法務向量庫]
    end
    
    subgraph "查詢處理層"
        J[使用者查詢] --> K[領域識別器]
        K --> L{選擇向量庫}
        L -->|金融| G
        L -->|醫療| H
        L -->|法務| I
    end
    
    subgraph "AI 推理層"
        G --> M[RetrievalQA Chain]
        H --> M
        I --> M
        M --> N[ChatOpenAI<br/>GPT-4 Turbo Preview]
    end
    
    subgraph "輸出層"
        N --> O[結構化回應]
        O --> P[引用溯源]
        P --> Q[最終答案]
    end
    
    style G fill:#e1f5fe
    style H fill:#f3e5f5
    style I fill:#e8f5e8
    style N fill:#fff3e0
```

## 技術棧說明

### 前端介面
- **Streamlit**: 快速原型開發
- **FastAPI**: 生產級 API 服務

### 核心技術
- **LangChain**: RAG 框架
- **OpenAI**: Embeddings + LLM
- **ChromaDB**: 向量資料庫
- **CharacterTextSplitter**: 文件分割

### 資料流程
1. **載入**: DirectoryLoader 載入各領域 .txt 檔案
2. **分割**: 1000 字元為單位的區塊分割
3. **向量化**: OpenAI embeddings 轉換為向量
4. **儲存**: 按領域分類存入 ChromaDB
5. **檢索**: 基於查詢語意進行向量相似度搜尋
6. **生成**: GPT-4 Turbo 生成自然語言回應

## 多模態處理能力

```mermaid
graph LR
    subgraph "MultiRAG 處理"
        A[文字輸入] --> D[統一 RAG 引擎]
        B[語音輸入] --> E[VideoSTT]
        C[影像輸入] --> F[OCR 處理]
        E --> D
        F --> D
        D --> G[多領域知識檢索]
        G --> H[統一回應格式]
    end
```

## 部署架構

```mermaid
graph TB
    subgraph "開發環境"
        A[Jupyter Notebook<br/>原型驗證]
    end
    
    subgraph "測試環境"
        B[Docker Container<br/>ChromaDB + API]
    end
    
    subgraph "生產環境"
        C[Kubernetes Cluster<br/>高可用部署]
        D[Load Balancer]
        E[Redis Cache]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
```

---
*技術展示：MVP-B 多產業 RAG 知識庫平台*
