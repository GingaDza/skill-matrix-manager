"""表示ユーティリティ"""
import logging
from datetime import datetime

class DisplayManager:
    """表示管理クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = logging.getLogger(__name__)
    
    def show_section(self, title: str):
        """セクションタイトルを表示"""
        print(f"\n{'='*20} {title} {'='*20}\n")
    
    def show_message(self, message: str, level: str = "info"):
        """メッセージを表示"""
        level_marks = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        mark = level_marks.get(level, "ℹ️")
        print(f"\n{mark} {message}\n")
        
        # ログにも記録
        log_method = getattr(self.logger, level, self.logger.info)
        log_method(message)
    
    def show_timestamp(self):
        """タイムスタンプを表示"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Timestamp (UTC): {timestamp}")

# シングルトンインスタンスを作成
display = DisplayManager()
