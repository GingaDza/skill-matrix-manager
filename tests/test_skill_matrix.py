import os
import sys
import unittest
import sqlite3
from datetime import datetime
import logging
from io import StringIO
from unittest.mock import patch

# テスト対象のモジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import SkillMatrixCLI

class TestSkillMatrixCLI(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行される設定"""
        self.test_db = ':memory:'
        self.app = SkillMatrixCLI()
        self.app.current_time = "2025-02-07 03:59:56"
        self.app.current_user = "GingaDza"
        
        # データベース接続
        self.app.conn = sqlite3.connect(self.test_db)
        self.app.cursor = self.app.conn.cursor()
        
        # テーブル作成とテストデータ投入
        self.setup_database()

    def setup_database(self):
        """データベースのセットアップ"""
        # テーブル作成
        self.app.cursor.executescript("""
            CREATE TABLE departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME,
                updated_at DATETIME,
                created_by TEXT,
                updated_by TEXT
            );
        """)

        # テストデータ投入
        self.app.cursor.execute("""
            INSERT INTO departments (
                name, description, is_active,
                created_at, updated_at, created_by, updated_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("開発部", "システム開発部門", 1, 
              self.app.current_time, self.app.current_time,
              self.app.current_user, self.app.current_user))
        
        self.app.conn.commit()

    def tearDown(self):
        """テスト後のクリーンアップ"""
        if self.app.conn:
            self.app.conn.close()

    @patch('builtins.input', return_value='\n')
    def test_list_departments(self, mock_input):
        """部署一覧表示のテスト"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.app.list_departments()
            output = fake_output.getvalue()
            self.assertIn("開発部", output)
            self.assertIn("システム開発部門", output)
            self.assertIn("アクティブ", output)

    @patch('builtins.input')
    def test_add_department(self, mock_input):
        """部署追加のテスト"""
        test_name = "テスト部署"
        test_description = "テスト用部署です"
        mock_input.side_effect = [test_name, test_description, '\n']
        
        with patch('sys.stdout', new=StringIO()):
            self.app.add_department()
        
        self.app.cursor.execute("""
            SELECT name, description, is_active 
            FROM departments 
            WHERE name = ?
        """, (test_name,))
        
        result = self.app.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_name)
        self.assertEqual(result[1], test_description)
        self.assertEqual(result[2], 1)

    @patch('builtins.input')
    def test_edit_department(self, mock_input):
        """部署編集のテスト"""
        dept_id = "1"
        new_name = "新開発部"
        new_description = "新しい説明"
        mock_input.side_effect = [dept_id, new_name, new_description, '\n']
        
        with patch('sys.stdout', new=StringIO()):
            self.app.edit_department()
            self.app.conn.commit()
        
        self.app.cursor.execute("""
            SELECT name, description 
            FROM departments 
            WHERE id = ?
        """, (dept_id,))
        
        result = self.app.cursor.fetchone()
        self.assertEqual(result[0], new_name)
        self.assertEqual(result[1], new_description)

    @patch('builtins.input')
    def test_delete_department(self, mock_input):
        """部署削除（無効化）のテスト"""
        dept_id = "1"
        mock_input.side_effect = [dept_id, '\n']
        
        with patch('sys.stdout', new=StringIO()):
            self.app.delete_department()
            self.app.conn.commit()
        
        self.app.cursor.execute("""
            SELECT is_active 
            FROM departments 
            WHERE id = ?
        """, (dept_id,))
        
        result = self.app.cursor.fetchone()
        self.assertEqual(result[0], 0)

    @patch('builtins.input', return_value='\n')
    def test_system_info(self, mock_input):
        """システム情報表示のテスト"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.app.show_system_info()
            output = fake_output.getvalue()
            
            self.assertIn("システム情報", output)
            self.assertIn("バージョン", output)
            self.assertIn("アクティブ部署数", output)

if __name__ == '__main__':
    unittest.main(verbosity=2)
