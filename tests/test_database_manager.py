"""データベースマネージャーのテスト"""
import unittest
from src.database.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """データベースマネージャーのテストケース"""
    
    def setUp(self):
        """テスト用のデータベースを準備"""
        self.db = DatabaseManager("test.db")
        
    def test_group_operations(self):
        """グループ操作のテスト"""
        # グループ追加
        self.assertTrue(self.db.add_group("TestGroup"))
        
        # ID取得
        group_id = self.db.get_group_id_by_name("TestGroup")
        self.assertIsNotNone(group_id)
        
        # グループ情報取得
        group_info = self.db.get_group_by_id(group_id)
        self.assertEqual(group_info[0], "TestGroup")
