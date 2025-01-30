# src/app/utils/db.py
from alembic.config import Config
from alembic import command
import os

def run_migrations():
    """データベースマイグレーションを実行する"""
    # alembic.iniのパスを取得
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../../alembic.ini'))
    
    try:
        # マイグレーションを実行
        command.upgrade(alembic_cfg, "head")
        print("Database migration completed successfully.")
    except Exception as e:
        print(f"Error during database migration: {e}")
        raise

def reset_database():
    """データベースをリセットする（開発環境用）"""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../../alembic.ini'))
    
    try:
        # データベースを最初の状態に戻す
        command.downgrade(alembic_cfg, "base")
        # 最新の状態にアップグレード
        command.upgrade(alembic_cfg, "head")
        print("Database reset completed successfully.")
    except Exception as e:
        print(f"Error during database reset: {e}")
        raise