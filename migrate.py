#!/usr/bin/env python3
"""マイグレーションコマンド実行スクリプト"""
import os
import sys
import logging
from pathlib import Path

# ロギング設定
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'migration.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def check_migration_files():
    """マイグレーションファイルの存在確認"""
    migrations_dir = Path("src/database/migrations")
    if not migrations_dir.exists():
        logger.error(f"マイグレーションディレクトリが見つかりません: {migrations_dir}")
        return False
    
    migration_files = list(migrations_dir.glob("V*__.py"))
    if not migration_files:
        logger.error("マイグレーションファイルが見つかりません")
        return False
    
    logger.info(f"検出されたマイグレーションファイル: {[f.name for f in migration_files]}")
    return True

try:
    from src.commands.migrate import run_migrations, rollback_migration
    
    def main():
        """メイン処理"""
        if not check_migration_files():
            sys.exit(1)
        
        db_path = os.getenv('DB_PATH', 'skill_matrix.db')
        logger.info(f"データベースパス: {db_path}")
        
        try:
            if len(sys.argv) > 1 and sys.argv[1] == "rollback":
                if len(sys.argv) != 3:
                    print("使用方法: python migrate.py rollback <version>")
                    sys.exit(1)
                rollback_migration(db_path, sys.argv[2])
            else:
                run_migrations(db_path)
        
        except Exception as e:
            logger.exception("マイグレーション処理でエラーが発生しました")
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    logger.error(f"必要なモジュールのインポートに失敗しました: {e}")
    print("\n以下のコマンドで必要なパッケージをインストールしてください：")
    print("pip install -r requirements.txt\n")
    sys.exit(1)
