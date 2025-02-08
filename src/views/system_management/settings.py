"""初期設定ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QListWidget, QPushButton,
    QInputDialog, QMessageBox, QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from ...database.database_manager import DatabaseManager

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        """初期化"""
        super().__init__(parent)
        
        # ロガー設定
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
        
        # レイアウトの初期化
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        
        # UIの構築
        self.init_ui()
        self.connect_signals()
        self.load_data()

    def init_ui(self):
        """UIの初期化"""
        # グループリスト
        group_box = self.create_group_list()
        self.main_layout.addWidget(group_box)
        
        # カテゴリーリスト
        category_box = self.create_category_lists()
        self.main_layout.addWidget(category_box)

    def create_group_list(self):
        """グループリストの作成"""
        group_box = QGroupBox("グループリスト")
        layout = QVBoxLayout()
        
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        button_layout.addWidget(self.add_group_btn)
        button_layout.addWidget(self.edit_group_btn)
        button_layout.addWidget(self.delete_group_btn)
        
        layout.addLayout(button_layout)
        group_box.setLayout(layout)
        return group_box

    def create_category_lists(self):
        """カテゴリーリストの作成"""
        category_box = QGroupBox("カテゴリー管理")
        layout = QVBoxLayout()
        
        # グループ選択
        group_select_layout = QHBoxLayout()
        group_select_layout.addWidget(QLabel("グループ:"))
        self.category_group_combo = QComboBox()
        group_select_layout.addWidget(self.category_group_combo)
        layout.addLayout(group_select_layout)
        
        # 親カテゴリー
        parent_box = QGroupBox("親カテゴリー")
        parent_layout = QVBoxLayout()
        self.parent_list = QListWidget()
        parent_layout.addWidget(self.parent_list)
        parent_box.setLayout(parent_layout)
        
        # 子カテゴリー
        child_box = QGroupBox("子カテゴリー")
        child_layout = QVBoxLayout()
        self.child_list = QListWidget()
        child_layout.addWidget(self.child_list)
        child_box.setLayout(child_layout)
        
        layout.addWidget(parent_box)
        layout.addWidget(child_box)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        self.add_category_btn = QPushButton("カテゴリー追加")
        self.edit_category_btn = QPushButton("カテゴリー編集")
        self.delete_category_btn = QPushButton("カテゴリー削除")
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_skill_btn = QPushButton("スキル編集")
        self.delete_skill_btn = QPushButton("スキル削除")
        self.new_tab_btn = QPushButton("新規タブ追加")
        
        button_layout.addWidget(self.add_category_btn)
        button_layout.addWidget(self.edit_category_btn)
        button_layout.addWidget(self.delete_category_btn)
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_skill_btn)
        button_layout.addWidget(self.delete_skill_btn)
        button_layout.addWidget(self.new_tab_btn)
        
        layout.addLayout(button_layout)
        category_box.setLayout(layout)
        return category_box

    # [その他のメソッドは前回と同じ]

