"""表示ユーティリティ
整形された出力を提供するモジュール
"""
from datetime import datetime
import os
import logging

class DisplayManager:
    """表示管理クラス
    
    アプリケーション全体で使用する表示機能を提供します。
    タイムスタンプやユーザー情報などの表示を標準化します。
    """
    
    def __init__(self):
        """DisplayManagerの初期化"""
        self.logger = logging.getLogger(__name__)
    
    def format_header(self, text: str) -> str:
        """ヘッダーテキストをフォーマット
        
        Args:
            text (str): フォーマットするテキスト
            
        Returns:
            str: フォーマットされたヘッダーテキスト
        """
        width = 80
        padding = (width - len(text)) // 2
        return f"{' ' * padding}{text}{' ' * padding}"
    
    def format_timestamp(self) -> str:
        """現在のタイムスタンプをフォーマット
        
        Returns:
            str: フォーマットされたタイムスタンプ
        """
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    def format_user(self) -> str:
        """現在のユーザー情報をフォーマット
        
        Returns:
            str: フォーマットされたユーザー情報
        """
        return os.getenv('USER', os.getenv('USERNAME', 'unknown'))
    
    def show_app_header(self):
        """アプリケーションヘッダーを表示"""
        print("\n" + "="*80)
        print(self.format_header("Skill Matrix Manager"))
        print("="*80)
        print(f"Started at: {self.format_timestamp()} (UTC)")
        print(f"User: {self.format_user()}")
        print("-"*80 + "\n")
    
    def show_section_header(self, section_name: str):
        """セクションヘッダーを表示
        
        Args:
            section_name (str): セクション名
        """
        print(f"\n{'-'*20} {section_name} {'-'*20}")
    
    def show_error(self, message: str):
        """エラーメッセージを表示
        
        Args:
            message (str): エラーメッセージ
        """
        self.logger.error(message)
        print(f"\nエラー: {message}\n")
    
    def show_success(self, message: str):
        """成功メッセージを表示
        
        Args:
            message (str): 成功メッセージ
        """
        self.logger.info(message)
        print(f"\n成功: {message}\n")

# シングルトンインスタンスを作成
display_manager = DisplayManager()

