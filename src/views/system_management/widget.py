"""システム管理ウィジェット"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .group_manager import GroupManager
from .category_manager import CategoryManager

class SystemManagementWidget(QWidget):
    """システム管理ウィジェットクラス"""
    
    def __init__(self, parent=None):
        """初期化"""
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タブウィジェットの作成
        tab_widget = QTabWidget()
        
        # グループ管理タブ
        group_manager = GroupManager()
        tab_widget.addTab(group_manager, "グループ管理")
        
        # カテゴリー管理タブ
        category_manager = CategoryManager()
        tab_widget.addTab(category_manager, "カテゴリー管理")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
