"""表示ユーティリティのテスト"""
import unittest
from datetime import datetime
from src.utils.display import DisplayManager

class TestDisplayManager(unittest.TestCase):
    """DisplayManagerのテスト"""
    
    def setUp(self):
        """テストの準備"""
        self.display = DisplayManager()
    
    def test_format_timestamp(self):
        """タイムスタンプのフォーマットをテスト"""
        timestamp = self.display.format_timestamp()
        try:
            datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.fail("タイムスタンプの形式が不正です")
    
    def test_format_user(self):
        """ユーザー情報のフォーマットをテスト"""
        user = self.display.format_user()
        self.assertIsInstance(user, str)
        self.assertGreater(len(user), 0)
    
    def test_format_header(self):
        """ヘッダーフォーマットのテスト"""
        text = "Test Header"
        header = self.display.format_header(text)
        self.assertIn(text, header)
        self.assertEqual(len(header), 80)

if __name__ == '__main__':
    unittest.main()
