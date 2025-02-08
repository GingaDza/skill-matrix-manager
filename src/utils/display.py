"""表示ユーティリティ"""
from datetime import datetime
import os
import logging

class DisplayManager:
    """表示管理クラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.width = 80
        self.app_name = "Skill Matrix Manager"
    
    def _center_text(self, text: str) -> str:
        """テキストを中央揃えにする"""
        padding = (self.width - len(text)) // 2
        return f"{' ' * padding}{text}{' ' * padding}"[:self.width]
    
    def show_app_info(self):
        """アプリケーション情報を表示"""
        print("\n" + "="*self.width)
        print(self._center_text(self.app_name))
        print("="*self.width)
        
        # 時刻とユーザー情報を表示
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        user = os.getenv('USER', os.getenv('USERNAME', 'unknown'))
        
        print(f"Time (UTC): {current_time}")
        print(f"User: {user}")
        print("-"*self.width + "\n")
    
    def show_section(self, title: str):
        """セクションタイトルを表示"""
        print(f"\n{'-'*20} {title} {'-'*20}\n")
    
    def show_message(self, message: str, level: str = "info"):
        """メッセージを表示

        Args:
            message (str): 表示するメッセージ
            level (str): メッセージレベル ("info", "success", "error", "warning")
        """
        prefix_map = {
            "info": "情報",
            "success": "成功",
            "error": "エラー",
            "warning": "警告"
        }
        prefix = prefix_map.get(level, "情報")
        print(f"\n{prefix}: {message}\n")
        
        # ログにも記録
        log_method = getattr(self.logger, level, self.logger.info)
        log_method(message)

# シングルトンインスタンスを作成
display = DisplayManager()
