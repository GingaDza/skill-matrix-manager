from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QMessageBox
)
from PyQt6.QtCore import Qt
from .tabs.system_management.initial_settings_tab import InitialSettingsTab
from .tabs.category.category_tab import CategoryTab
from ..database.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """アプリケーションのメインウィンドウ"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        self.setWindowTitle("スキルマトリックス管理システム")
        self.resize(1200, 800)
        
        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインレイアウト
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # システム設定タブ
        self.system_tab = InitialSettingsTab(self)
        self.tab_widget.addTab(self.system_tab, "システム管理")
        
        # カテゴリータブ
        self.category_tab = CategoryTab(self)
        self.tab_widget.addTab(self.category_tab, "カテゴリー")
        
        # ステータスバー
        self.statusBar().showMessage("準備完了")

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        reply = QMessageBox.question(
            self,
            '確認',
            'アプリケーションを終了しますか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
