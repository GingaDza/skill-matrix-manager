"""システム管理ウィジェット"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .group_manager import GroupManager
from .category_manager import CategoryManager
from ...database.database_manager import DatabaseManager

class SystemManagementWidget(QWidget):
    """システム管理ウィジェットクラス"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャー
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self._db = db_manager
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タブウィジェットの作成
        tab_widget = QTabWidget()
        
        # グループ管理タブ
        group_manager = GroupManager(self._db)
        tab_widget.addTab(group_manager, "グループ管理")
        
        # カテゴリー管理タブ
        category_manager = CategoryManager(self._db)
        tab_widget.addTab(category_manager, "カテゴリー管理")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
