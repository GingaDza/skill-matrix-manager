# tests/test_migrations.py
import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models import Base, User, Category, Skill, SkillAssessment
from src.app.utils.db import run_migrations, reset_database

class TestMigrations(unittest.TestCase):
    def setUp(self):
        # テスト用のデータベースURLを設定
        self.test_db_url = "sqlite:///test_skill_matrix.db"
        # 環境変数でデータベースURLを上書き
        os.environ['DATABASE_URL'] = self.test_db_url
        
    def test_migrations(self):
        # マイグレーションを実行
        run_migrations()
        
        # データベース接続を確認
        engine = create_engine(self.test_db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # テーブルが正しく作成されているか確認
        self.assertTrue(engine.has_table('users'))
        self.assertTrue(engine.has_table('categories'))
        self.assertTrue(engine.has_table('skills'))
        self.assertTrue(engine.has_table('skill_assessments'))
        
        session.close()
    
    def tearDown(self):
        # テスト用データベースを削除
        if os.path.exists("test_skill_matrix.db"):
            os.remove("test_skill_matrix.db")