"""設定ウィジェットの基本クラス"""
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QListWidget
)
from ..base.base_widget import BaseWidget
from .group_manager import GroupManagerMixin
from .category_manager import CategoryManagerMixin
from .skill_manager import SkillManagerMixin

class SettingsWidgetBase(BaseWidget, GroupManagerMixin, CategoryManagerMixin, SkillManagerMixin):
    """設定ウィジェットの基本クラス"""
    
    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャー
            parent: 親ウィジェット
        """
        super().__init__(db_manager=db_manager, parent=parent)
        self.setup()  # UIの初期化とシグナルの接続
        self.logger.info("SettingsWidgetBase initialized")

    def init_ui(self):
        """UIを初期化する"""
        # メインレイアウト
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # グループ選択部分
        group_layout = QHBoxLayout()
        self.category_group_combo = QComboBox()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        group_layout.addWidget(self.category_group_combo)
        group_layout.addWidget(self.add_group_btn)
        group_layout.addWidget(self.edit_group_btn)
        group_layout.addWidget(self.delete_group_btn)
        
        main_layout.addLayout(group_layout)

        # カテゴリーとスキルのリスト部分
        list_layout = QHBoxLayout()
        
        # カテゴリー部分
        category_layout = QVBoxLayout()
        self.parent_list = QListWidget()
        self.add_parent_btn = QPushButton("追加")
        self.edit_parent_btn = QPushButton("編集")
        self.delete_parent_btn = QPushButton("削除")
        
        category_layout.addWidget(self.parent_list)
        
        category_btn_layout = QHBoxLayout()
        category_btn_layout.addWidget(self.add_parent_btn)
        category_btn_layout.addWidget(self.edit_parent_btn)
        category_btn_layout.addWidget(self.delete_parent_btn)
        category_layout.addLayout(category_btn_layout)
        
        # スキル部分
        skill_layout = QVBoxLayout()
        self.child_list = QListWidget()
        self.add_child_btn = QPushButton("追加")
        self.edit_child_btn = QPushButton("編集")
        self.delete_child_btn = QPushButton("削除")
        
        skill_layout.addWidget(self.child_list)
        
        skill_btn_layout = QHBoxLayout()
        skill_btn_layout.addWidget(self.add_child_btn)
        skill_btn_layout.addWidget(self.edit_child_btn)
        skill_btn_layout.addWidget(self.delete_child_btn)
        skill_layout.addLayout(skill_btn_layout)
        
        list_layout.addLayout(category_layout)
        list_layout.addLayout(skill_layout)
        
        main_layout.addLayout(list_layout)

        # 初期データの読み込み
        self._load_initial_data()

    def _load_initial_data(self):
        """初期データを読み込む"""
        try:
            groups = self._db_manager.get_groups()
            self.logger.info(f"読み込まれたグループ: {groups}")
            
            self.category_group_combo.clear()
            self.category_group_combo.addItems(groups)
            
        except Exception as e:
            self.logger.exception("初期データ読み込みエラー")

    def _connect_signals(self):
        """シグナルを接続する"""
        # グループ関連
        self.category_group_combo.currentIndexChanged.connect(self._on_group_selected)
        self.add_group_btn.clicked.connect(self._on_add_group)
        self.edit_group_btn.clicked.connect(self._on_edit_group)
        self.delete_group_btn.clicked.connect(self._on_delete_group)
        
        # カテゴリー関連
        self.parent_list.currentRowChanged.connect(self._on_parent_selected)
        self.add_parent_btn.clicked.connect(self._on_add_category)
        self.edit_parent_btn.clicked.connect(self._on_edit_category)
        self.delete_parent_btn.clicked.connect(self._on_delete_category)
        
        # スキル関連
        self.add_child_btn.clicked.connect(self._on_add_skill)
        self.edit_child_btn.clicked.connect(self._on_edit_skill)
        self.delete_child_btn.clicked.connect(self._on_delete_skill)
