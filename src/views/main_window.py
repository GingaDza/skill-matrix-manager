"""メインウィンドウの実装"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QTabWidget, QPushButton, QMessageBox
)
from PyQt5 import QtCore
from .system_management.group_manager import GroupManager
from .system_management.category_manager import CategoryManager
from .skill_management.skill_viewer import SkillViewer
from ..database.database_manager import DatabaseManager
import logging

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""

    def __init__(self, db_manager: DatabaseManager):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャーのインスタンス
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()
        self.logger.info("初期データの読み込みを開始")

    def _init_ui(self):
        """UIの初期化"""
        self.setWindowTitle('スキルマトリックスマネージャー')
        self.setGeometry(100, 100, 800, 600)

        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # システム管理タブ
        system_tab = QWidget()
        system_layout = QVBoxLayout(system_tab)
        
        # グループ管理
        self.group_manager = GroupManager(self._db_manager)
        system_layout.addWidget(self.group_manager)
        
        # カテゴリー管理
        self.category_manager = CategoryManager(self._db_manager)
        system_layout.addWidget(self.category_manager)

        self.tab_widget.addTab(system_tab, "システム管理")

        # スキル管理タブ
        skill_tab = QWidget()
        skill_layout = QVBoxLayout(skill_tab)
        
        # スキルビューア
        self.skill_viewer = SkillViewer(self._db_manager)
        skill_layout.addWidget(self.skill_viewer)

        self.tab_widget.addTab(skill_tab, "スキル管理")

    def closeEvent(self, event):
        """
        ウィンドウを閉じる際の処理
        
        Args:
            event: クローズイベント
        """
        reply = QMessageBox.question(
            self, 'アプリケーションの終了',
            "アプリケーションを終了しますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.logger.info("アプリケーションを終了します")
            event.accept()
        else:
            event.ignore()
