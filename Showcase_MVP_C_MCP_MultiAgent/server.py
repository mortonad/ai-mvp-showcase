from mcp.server.fastmcp import FastMCP

# 建立一個名為 "CompanyContext" 的 MCP 伺服器
mcp = FastMCP("CompanyContext")

@mcp.tool()
def get_customer_info(customer_id: str) -> str:
    """查詢客戶的基本資料與歷史互動記錄。"""
    # 這裡未來可以對接真正的資料庫
    mock_db = {
        "C001": "客戶：吉永建設。狀態：洽談中。重點：對 AI 雙引擎套件有興趣。",
        "C002": "客戶：齊虹實業。狀態：已結案。重點：AI 標案助手效果良好。"
    }
    return mock_db.get(customer_id, "找不到該客戶資料。")

@mcp.tool()
def get_market_trends(industry: str) -> str:
    """查詢特定產業的 AI 導入趨勢。"""
    trends = {
        "medical": "醫美產業正轉向非侵入式診斷 AI。",
        "finance": "金融業正高度關注非同步推論排程技術。"
    }
    return trends.get(industry, "目前無該產業的特定趨勢數據。")

if __name__ == "__main__":
    mcp.run()
