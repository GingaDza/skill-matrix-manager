"""データベースマネージャーのテスト"""
import unittest
import os
from src.database.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """DatabaseManagerのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.db_path = "test_skill_matrix.db"
        self.db = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_add_group(self):
        """グループ追加のテスト"""
        group_name = "テストグループ"
        self.db.add_group(group_name)
        groups = self.db.get_groups()
        self.assertIn(group_name, groups)
    
    # ... 他のテスト
