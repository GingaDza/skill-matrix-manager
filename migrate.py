#!/usr/bin/env python3
"""マイグレーションコマンド実行スクリプト"""
import sys
import logging
from src.utils.logging_config import setup_logging
from src.commands.migrate import run_migrations, rollback_migration
from src.config import Config

def main():
    """メイン処理"""
    # 設定を読み込み
    config = Config.from_env()
    
    # ロギングを設定
    setup_logging(config.log_dir)
    logger = logging.getLogger(__name__)
    
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "rollback":
            if len(sys.argv) != 3:
                print("使用方法: python migrate.py rollback <version>")
                sys.exit(1)
            rollback_migration(config.db.path, sys.argv[2])
        else:
            run_migrations(config.db.path)
    
    except Exception as e:
        logger.exception("マイグレーション処理でエラーが発生しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
