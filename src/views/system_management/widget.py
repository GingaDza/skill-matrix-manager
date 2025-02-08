"""システム管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from .group_manager import GroupManager
from .category_manager import CategoryManager
from .skill_manager import SkillManager
from ..data_management import DataManagementWidget
from ..custom_tab import CategoryTab
from ...database.database_manager import DatabaseManager
import logging

class SystemManagementWidget(QWidget):
    """システム管理ウィジェットクラス"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db = db_manager
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        
        # 初期設定タブ
        settings_tab = QWidget()
        settings_layout = QHBoxLayout()
        
        # グループ管理
        self.group_manager = GroupManager(self._db)
        settings_layout.addWidget(self.group_manager)
        
        # カテゴリー管理
        self.category_manager = CategoryManager(self._db)
        settings_layout.addWidget(self.category_manager)
        
        # スキル管理
        self.skill_manager = SkillManager(self._db)
        settings_layout.addWidget(self.skill_manager)
        
        settings_tab.setLayout(settings_layout)
        self.tab_widget.addTab(settings_tab, "初期設定")
        
        # データ管理タブ
        data_tab = DataManagementWidget(self._db)
        self.tab_widget.addTab(data_tab, "データ管理")
        
        layout.addWidget(self.tab_widget)
        
        # 新規タブ追加ボタン
        add_tab_frame = QFrame()
        add_tab_frame.setFrameStyle(QFrame.StyledPanel)
        add_tab_layout = QHBoxLayout()
        
        add_tab_btn = QPushButton("選択したカテゴリーで新規タブを追加")
        add_tab_btn.clicked.connect(self._add_custom_tab)
        add_tab_layout.addWidget(add_tab_btn)
        
        add_tab_frame.setLayout(add_tab_layout)
        layout.addWidget(add_tab_frame)
        
        self.setLayout(layout)
    
    def get_selected_group(self) -> str:
        """選択中のグループ名を取得"""
        return self.group_manager.get_selected_group()
    
    def get_selected_category(self) -> str:
        """選択中のカテゴリー名を取得"""
        return self.category_manager.get_selected_category()
    
    def _add_custom_tab(self):
        """新規カスタムタブを追加"""
        group_name = self.get_selected_group()
        category_name = self.get_selected_category()
        
        if not group_name or not category_name:
            QMessageBox.warning(
                self,
                "警告",
                "新規タブを追加するグループとカテゴリーを選択してください"
            )
            return
            
        try:
            # メインウィンドウのタブウィジェットにカスタムタブを追加
            main_window = self.window()
            if main_window:
                category_tab = CategoryTab(
                    self._db,
                    group_name,
                    category_name
                )
                main_window.add_custom_tab(category_name, category_tab)
                self.logger.info(
                    f"新規タブを追加しました: {category_name} "
                    f"(グループ: {group_name})"
                )
        except Exception as e:
            self.logger.exception("新規タブの追加に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"新規タブの追加に失敗しました: {str(e)}"
            )
