"""データベースマネージャーのテスト"""
import unittest
import os
from src.database.database_manager import DatabaseManager
from src.database.exceptions import EntityNotFoundError, DatabaseError

class TestDatabaseManager(unittest.TestCase):
    """データベースマネージャーのテストケース"""
    
    def setUp(self):
        """テスト用のデータベースを準備"""
        self.test_db = "test.db"
        # 古いテストDBがあれば削除
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.db = DatabaseManager(self.test_db)
        
    def tearDown(self):
        """テスト用のデータベースを削除"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_group_operations(self):
        """グループ操作のテスト"""
        # グループ追加
        self.assertTrue(self.db.add_group("TestGroup"))
        
        # 重複グループの追加をテスト
        self.assertFalse(self.db.add_group("TestGroup"))
        
        # ID取得
        group_id = self.db.get_group_id_by_name("TestGroup")
        self.assertIsNotNone(group_id)
        
        # 存在しないグループのID取得
        with self.assertRaises(EntityNotFoundError):
            self.db.get_group_id_by_name("NonExistentGroup")
        
        # グループ情報取得
        group_info = self.db.get_group_by_id(group_id)
        self.assertEqual(group_info[0], "TestGroup")
        
        # 存在しないIDのグループ情報取得
        with self.assertRaises(EntityNotFoundError):
            self.db.get_group_by_id(999)

if __name__ == '__main__':
    unittest.main()
