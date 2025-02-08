"""システム管理ウィジェット"""
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .settings import SettingsWidget

class SystemManagementWidget(QWidget):
    """システム管理ウィジェット"""
    
    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャー
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self._db_manager = db_manager
        self.tab_widget = QTabWidget()
        self.init_ui()

    def init_ui(self):
        """UIを初期化する"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 設定タブを作成
        settings = SettingsWidget(self._db_manager, self.tab_widget)
        self.tab_widget.addTab(settings, "設定")
        
        layout.addWidget(self.tab_widget)
