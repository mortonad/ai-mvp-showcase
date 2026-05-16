"""
非同步 AI 推論排程器
- 模擬 Redis/RabbitMQ 任務佇列（使用 dict + threading）
- 支援任務提交、狀態查詢、結果取回
- 展示 BackgroundTasks + 任務生命週期管理
"""
import time
import threading
import uuid
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResult:
    """任務結果封裝"""
    def __init__(self, task_id: str, task_type: str, params: dict):
        self.task_id = task_id
        self.task_type = task_type
        self.params = params
        self.status = TaskStatus.QUEUED
        self.created_at = datetime.now().isoformat()
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.result: Optional[dict] = None
        self.error: Optional[str] = None
        self.progress: int = 0

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "params": self.params,
            "status": self.status.value,
            "progress": self.progress,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error,
        }


# ── 模擬任務佇列（替代 Redis/RabbitMQ） ──────────────
class InMemoryTaskQueue:
    """
    記憶體中的任務佇列
    在生產環境中可替換為 Redis + Celery 或 RabbitMQ
    """
    
    def __init__(self):
        self._tasks: dict[str, TaskResult] = {}
        self._lock = threading.Lock()

    def submit(self, task_type: str, params: dict) -> str:
        """提交新任務"""
        task_id = str(uuid.uuid4())[:8]
        task = TaskResult(task_id, task_type, params)
        
        with self._lock:
            self._tasks[task_id] = task
        
        return task_id

    def get_task(self, task_id: str) -> Optional[TaskResult]:
        """查詢任務狀態"""
        return self._tasks.get(task_id)

    def update_task(self, task_id: str, **kwargs):
        """更新任務狀態"""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                for key, value in kwargs.items():
                    setattr(task, key, value)

    def list_tasks(self, limit: int = 20) -> list[dict]:
        """列出最近的任務"""
        tasks = sorted(
            self._tasks.values(),
            key=lambda t: t.created_at,
            reverse=True,
        )
        return [t.to_dict() for t in tasks[:limit]]


# ── 全域任務佇列實例 ─────────────────────────────────
task_queue = InMemoryTaskQueue()


# ── 模擬推論任務 ─────────────────────────────────────

def run_backtest(symbol: str, task_id: Optional[str] = None):
    """
    模擬股市策略回測任務
    - 耗時任務（模擬 5 秒運算）
    - 產出結構化回測結果
    """
    if task_id:
        task_queue.update_task(
            task_id,
            status=TaskStatus.RUNNING,
            started_at=datetime.now().isoformat(),
            progress=0,
        )
    
    try:
        # 模擬回測過程
        stages = [
            (20, "載入歷史價格資料"),
            (40, "計算技術指標 (MA / RSI / MACD)"),
            (60, "執行策略回測"),
            (80, "計算績效指標"),
            (100, "生成回測報告"),
        ]
        
        for progress, stage in stages:
            time.sleep(1)  # 模擬運算耗時
            if task_id:
                task_queue.update_task(task_id, progress=progress)
        
        # 模擬回測結果
        result = {
            "symbol": symbol,
            "strategy": "MA Crossover (短期 5 日 × 長期 20 日)",
            "backtest_period": "2025-01-01 ~ 2026-05-15",
            "total_trades": 42,
            "win_rate": "61.9%",
            "total_return": "+23.7%",
            "max_drawdown": "-8.3%",
            "sharpe_ratio": 1.42,
            "annualized_return": "+17.1%",
            "benchmark_return": "+12.5%",
            "alpha": "+4.6%",
        }
        
        if task_id:
            task_queue.update_task(
                task_id,
                status=TaskStatus.COMPLETED,
                completed_at=datetime.now().isoformat(),
                result=result,
                progress=100,
            )
        
        return result
    
    except Exception as e:
        if task_id:
            task_queue.update_task(
                task_id,
                status=TaskStatus.FAILED,
                error=str(e),
                completed_at=datetime.now().isoformat(),
            )
        raise


def run_sentiment_analysis(text: str, task_id: Optional[str] = None):
    """
    模擬 NLP 情緒分析任務
    """
    if task_id:
        task_queue.update_task(
            task_id,
            status=TaskStatus.RUNNING,
            started_at=datetime.now().isoformat(),
        )
    
    try:
        time.sleep(3)  # 模擬推論耗時
        
        result = {
            "text": text[:100],
            "sentiment": "positive",
            "confidence": 0.87,
            "emotions": {
                "joy": 0.65,
                "trust": 0.20,
                "anticipation": 0.10,
                "surprise": 0.05,
            },
            "key_phrases": ["AI 應用", "市場趨勢", "效率提升"],
        }
        
        if task_id:
            task_queue.update_task(
                task_id,
                status=TaskStatus.COMPLETED,
                completed_at=datetime.now().isoformat(),
                result=result,
                progress=100,
            )
        
        return result
    
    except Exception as e:
        if task_id:
            task_queue.update_task(
                task_id,
                status=TaskStatus.FAILED,
                error=str(e),
            )
        raise


# ── 任務路由器 ───────────────────────────────────────

TASK_RUNNERS = {
    "backtest": run_backtest,
    "sentiment": run_sentiment_analysis,
}


def execute_task_async(task_id: str, task_type: str, params: dict):
    """在背景執行緒中執行任務"""
    runner = TASK_RUNNERS.get(task_type)
    if runner:
        runner(task_id=task_id, **params)
    else:
        task_queue.update_task(
            task_id,
            status=TaskStatus.FAILED,
            error=f"Unknown task type: {task_type}",
        )
