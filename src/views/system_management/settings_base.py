"""初期設定ウィジェットのベースクラス"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QListWidget, QPushButton,
    QInputDialog, QMessageBox, QLabel, QComboBox,
    QMainWindow
)
from PyQt6.QtCore import Qt
from ...database.database_manager import DatabaseManager

class SettingsWidgetBase(QWidget):
    """初期設定タブのベースウィジェット"""
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        
        # UI要素の初期化
        self.group_list = None
        self.category_group_combo = None
        self.parent_list = None
        self.child_list = None
        
        # ボタンの初期化
        self.add_group_btn = None
        self.edit_group_btn = None
        self.delete_group_btn = None
        self.add_category_btn = None
        self.edit_category_btn = None
        self.delete_category_btn = None
        self.add_skill_btn = None
        self.edit_skill_btn = None
        self.delete_skill_btn = None
        self.new_tab_btn = None
        
        # メインレイアウト
        self.main_layout = QHBoxLayout(self)
        
        self.logger.info("SettingsWidgetBase initialized")

    def _load_data(self):
        """データの読み込み"""
        try:
            # グループの読み込み
            groups = self._db_manager.get_groups()
            self.logger.info(f"読み込まれたグループ: {groups}")
            
            # グループリストの更新
            self.group_list.clear()
            self.group_list.addItems(groups)
            
            # グループコンボボックスの更新
            self.category_group_combo.clear()
            self.category_group_combo.addItems(groups)
            
            # 最初のグループのカテゴリーを表示
            if groups:
                self._on_category_group_changed(groups[0])
                
        except Exception as e:
            self.logger.exception("データ読み込みエラー")
            QMessageBox.critical(
                self,
                "エラー",
                "データの読み込みに失敗しました。"
            )