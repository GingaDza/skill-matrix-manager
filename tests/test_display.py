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
