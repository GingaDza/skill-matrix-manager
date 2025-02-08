"""表示ユーティリティのテスト"""
import unittest
from io import StringIO
import sys
from src.utils.display import DisplayManager

class TestDisplayManager(unittest.TestCase):
    def setUp(self):
        self.display = DisplayManager()
        self.held_output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.held_output
    
    def tearDown(self):
        sys.stdout = self.old_stdout
    
    def test_app_info_format(self):
        """アプリケーション情報の表示形式をテスト"""
        self.display.show_app_info()
        output = self.held_output.getvalue()
        
        # 基本的なフォーマットをチェック
        self.assertIn(self.display.app_name, output)
        self.assertIn("Time (UTC):", output)
        self.assertIn("User:", output)
        
        # 区切り線をチェック
        self.assertIn("="*self.display.width, output)
    
    def test_message_display(self):
        """メッセージ表示をテスト"""
        test_message = "テストメッセージ"
        self.display.show_message(test_message, "success")
        output = self.held_output.getvalue()
        
        self.assertIn("成功:", output)
        self.assertIn(test_message, output)

if __name__ == '__main__':
    unittest.main()
