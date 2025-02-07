#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.database.database_manager import DatabaseManager

def main():
    """アプリケーションのメインエントリーポイント"""
    # データベースの初期化
    db_manager = DatabaseManager()
    db_manager.initialize_database()

    # アプリケーションの起動
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
