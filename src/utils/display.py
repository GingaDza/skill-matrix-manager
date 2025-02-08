"""表示ユーティリティ"""
from datetime import datetime
import os

class DisplayManager:
    """表示管理クラス"""
    
    @staticmethod
    def format_timestamp() -> str:
        """タイムスタンプをフォーマット"""
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def format_user() -> str:
        """ユーザー情報をフォーマット"""
        return os.getenv('USER', os.getenv('USERNAME', 'unknown'))
    
    @classmethod
    def show_info(cls):
        """情報を表示"""
        print(f"Timestamp (UTC): {cls.format_timestamp()}")
        print(f"User: {cls.format_user()}")

display_manager = DisplayManager()
