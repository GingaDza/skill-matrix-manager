#!/usr/bin/env python3
import sys
import logging
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.database.database_manager import DatabaseManager
from src.utils.time_utils import TimeProvider

def setup_logging():
    """ロギングの設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """アプリケーションのメインエントリーポイント"""
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # データベースの初期化
        logger.info("データベースの初期化を開始")
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        logger.info("データベースの初期化が完了しました")

        # 現在のユーザーを設定
        TimeProvider.set_current_user("GingaDza")
        logger.info(f"現在のユーザー: {TimeProvider.get_current_user()}")
        logger.info(f"現在の時刻: {TimeProvider.get_formatted_time()}")

        # アプリケーションの起動
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"アプリケーションの起動中にエラーが発生: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
