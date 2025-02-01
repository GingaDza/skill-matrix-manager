"""
Main Window implementation
Created: 2025-01-31 23:49:00
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QComboBox, QListWidget, QPushButton,
    QTreeWidget, QSplitter
)
from PySide6.QtCore import Qt
from ..models.data_manager import DataManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skill Matrix Manager")
        self.resize(1200, 800)
        self.data_manager = DataManager()
        
        # メインウィジェットとレイアウトの設定
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # タブウィジェットの設定
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # スキルマトリクスタブの追加
        self.skill_matrix_tab = SkillMatrixTab(self.data_manager)
        self.tab_widget.addTab(self.skill_matrix_tab, "Skill Matrix")

class SkillMatrixTab(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        
        # レイアウトの設定
        layout = QHBoxLayout(self)
        
        # スプリッター（左右パネルを分割）
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左パネル（ユーザー管理）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # グループ選択コンボボックス
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        left_layout.addWidget(self.group_combo)
        
        # ユーザーリスト
        self.user_list = QListWidget()
        left_layout.addWidget(self.user_list)
        
        # ユーザー管理ボタン
        user_buttons_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("Add User")
        self.edit_user_btn = QPushButton("Edit User")
        self.delete_user_btn = QPushButton("Delete User")
        
        user_buttons_layout.addWidget(self.add_user_btn)
        user_buttons_layout.addWidget(self.edit_user_btn)
        user_buttons_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(user_buttons_layout)
        
        # 右パネル（グループ/カテゴリー/スキル管理）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # グループ管理セクション
        group_section = QWidget()
        group_layout = QVBoxLayout(group_section)
        self.group_tree = QTreeWidget()
        group_layout.addWidget(self.group_tree)
        
        group_buttons_layout = QHBoxLayout()
        self.add_group_btn = QPushButton("Add Group")
        self.edit_group_btn = QPushButton("Edit Group")
        self.delete_group_btn = QPushButton("Delete Group")
        
        group_buttons_layout.addWidget(self.add_group_btn)
        group_buttons_layout.addWidget(self.edit_group_btn)
        group_buttons_layout.addWidget(self.delete_group_btn)
        group_layout.addLayout(group_buttons_layout)
        
        # カテゴリー/スキルツリー
        self.category_skill_tree = QTreeWidget()
        right_layout.addWidget(self.category_skill_tree)
        
        # カテゴリー/スキル管理ボタン
        cs_buttons_layout = QHBoxLayout()
        self.add_category_btn = QPushButton("Add Category")
        self.add_skill_btn = QPushButton("Add Skill")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        
        cs_buttons_layout.addWidget(self.add_category_btn)
        cs_buttons_layout.addWidget(self.add_skill_btn)
        cs_buttons_layout.addWidget(self.edit_btn)
        cs_buttons_layout.addWidget(self.delete_btn)
        right_layout.addLayout(cs_buttons_layout)
        
        # スプリッターにパネルを追加
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # シグナル/スロット接続
        self._connect_signals()
        
        # 初期データの読み込み
        self._load_initial_data()
    
    def _connect_signals(self):
        """シグナル/スロットの接続"""
        # ユーザー管理
        self.add_user_btn.clicked.connect(self.on_add_user)
        self.edit_user_btn.clicked.connect(self.on_edit_user)
        self.delete_user_btn.clicked.connect(self.on_delete_user)
        
        # グループ管理
        self.add_group_btn.clicked.connect(self.on_add_group)
        self.edit_group_btn.clicked.connect(self.on_edit_group)
        self.delete_group_btn.clicked.connect(self.on_delete_group)
        
        # カテゴリー/スキル管理
        self.add_category_btn.clicked.connect(self.on_add_category)
        self.add_skill_btn.clicked.connect(self.on_add_skill)
        self.edit_btn.clicked.connect(self.on_edit_item)
        self.delete_btn.clicked.connect(self.on_delete_item)
    
    def _load_initial_data(self):
        """初期データの読み込み"""
        # グループの読み込み
        groups = self.data_manager.get_all_groups()
        self.group_combo.clear()
        for group in groups:
            self.group_combo.addItem(group.name, group.id)
    
    def on_group_changed(self, index):
        """グループ選択時の処理"""
        if index < 0:
            return
        group_id = self.group_combo.currentData()
        self._update_user_list(group_id)
        self._update_category_skill_tree(group_id)