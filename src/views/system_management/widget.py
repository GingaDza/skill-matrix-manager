"""システム管理ウィジェット"""
import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .settings import SettingsWidget
from .io import IOWidget
from .info import InfoWidget
from ...database.database_manager import DatabaseManager

class SystemManagementWidget(QWidget):
    """システム管理タブのメインウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # サブタブの作成
        self.tab_widget = QTabWidget(self)
        
        # 初期設定タブ
        settings = SettingsWidget(self._db_manager, self.tab_widget)
        self.tab_widget.addTab(settings, "初期設定")
        
        # データ入出力タブ
        io = IOWidget(self._db_manager, self.tab_widget)
        self.tab_widget.addTab(io, "データ入出力")
        
        # システム情報タブ
        info = InfoWidget(self._db_manager, self.tab_widget)
        self.tab_widget.addTab(info, "システム情報")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
