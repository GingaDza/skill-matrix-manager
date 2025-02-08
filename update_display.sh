#!/bin/bash

echo "Updating display utilities..."

# ディレクトリ作成
mkdir -p src/utils

# display.pyの更新
cat > src/utils/display.py << 'EOL'
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
EOL

# app.pyの更新
cat > src/app.py << 'EOL'
"""アプリケーションのメインモジュール"""
import sys
import logging
from typing import List
from .utils.display import display_manager
from .database import DatabaseManager

class App:
    """アプリケーションクラス"""
    
    def __init__(self, argv: List[str]):
        """初期化"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("アプリケーションを初期化中...")
        display_manager.show_info()
        self._db = DatabaseManager()
    
    def run(self):
        """アプリケーションを実行"""
        try:
            self.logger.info("アプリケーションを実行中...")
        except Exception as e:
            self.logger.exception("予期せぬエラーが発生しました")
            raise
EOL

# テストの作成
mkdir -p tests
cat > tests/test_display.py << 'EOL'
"""表示ユーティリティのテスト"""
import unittest
from datetime import datetime
from src.utils.display import DisplayManager

class TestDisplayManager(unittest.TestCase):
    """DisplayManagerのテスト"""
    
    def test_format_timestamp(self):
        """タイムスタンプのフォーマットをテスト"""
        timestamp = DisplayManager.format_timestamp()
        # タイムスタンプが正しい形式かチェック
        try:
            datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.fail("タイムスタンプの形式が不正です")
    
    def test_format_user(self):
        """ユーザー情報のフォーマットをテスト"""
        user = DisplayManager.format_user()
        self.assertIsInstance(user, str)
        self.assertGreater(len(user), 0)

if __name__ == '__main__':
    unittest.main()
EOL

echo "ファイルの更新が完了しました"

# Git操作
git add src/utils/display.py src/app.py tests/test_display.py
git commit -m "refactor: 表示機能をDisplayManagerクラスに整理

- DisplayManagerクラスを作成
- タイムスタンプと表示形式を改善
- ユニットテストを追加
- コードの構造を改善
- エラー処理を強化"

git push origin feature/category-tab

echo "更新が完了しました"
