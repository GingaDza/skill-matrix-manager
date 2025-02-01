# src/desktop/main.py
"""
Main application entry point
Created: 2025-01-31 13:37:42
Author: GingaDza
"""
import sys
from datetime import datetime
import os
from PySide6.QtWidgets import QApplication
from .gui.main_window import MainWindow
from .models.data_manager import DataManager

# MacOS特有の設定
os.environ['QT_MAC_WANTS_LAYER'] = '1'

class SkillMatrixApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        # アプリケーション情報の表示
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print("Starting Skill Matrix Manager...")
        print(f"Current Time (UTC): {current_time}")
        print(f"Current User: GingaDza")
        
        # メインウィンドウの設定と表示
        self.main_window = MainWindow()
        self.main_window.show()

def main():
    try:
        app = SkillMatrixApp(sys.argv)
        return app.exec()
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())