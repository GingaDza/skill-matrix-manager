"""設定ウィジェットの基本クラス"""
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QListWidget,
    QLabel
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
        group_layout = QVBoxLayout()
        group_label = QLabel("グループ:")
        group_controls = QHBoxLayout()
        
        self.category_group_combo = QComboBox()
        self.category_group_combo.setPlaceholderText("グループを選択してください")
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        group_controls.addWidget(self.category_group_combo)
        group_controls.addWidget(self.add_group_btn)
        group_controls.addWidget(self.edit_group_btn)
        group_controls.addWidget(self.delete_group_btn)
        
        group_layout.addWidget(group_label)
        group_layout.addLayout(group_controls)
        main_layout.addLayout(group_layout)

        # カテゴリーとスキルのリスト部分
        list_layout = QHBoxLayout()
        
        # カテゴリー部分
        category_layout = QVBoxLayout()
        category_label = QLabel("カテゴリー:")
        self.parent_list = QListWidget()
        self.parent_list.setPlaceholderText("グループを選択してください")
        
        category_btn_layout = QHBoxLayout()
        self.add_parent_btn = QPushButton("追加")
        self.edit_parent_btn = QPushButton("編集")
        self.delete_parent_btn = QPushButton("削除")
        
        category_btn_layout.addWidget(self.add_parent_btn)
        category_btn_layout.addWidget(self.edit_parent_btn)
        category_btn_layout.addWidget(self.delete_parent_btn)
        
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.parent_list)
        category_layout.addLayout(category_btn_layout)
        
        # スキル部分
        skill_layout = QVBoxLayout()
        skill_label = QLabel("スキル:")
        self.child_list = QListWidget()
        self.child_list.setPlaceholderText("カテゴリーを選択してください")
        
        skill_btn_layout = QHBoxLayout()
        self.add_child_btn = QPushButton("追加")
        self.edit_child_btn = QPushButton("編集")
        self.delete_child_btn = QPushButton("削除")
        
        skill_btn_layout.addWidget(self.add_child_btn)
        skill_btn_layout.addWidget(self.edit_child_btn)
        skill_btn_layout.addWidget(self.delete_child_btn)
        
        skill_layout.addWidget(skill_label)
        skill_layout.addWidget(self.child_list)
        skill_layout.addLayout(skill_btn_layout)
        
        list_layout.addLayout(category_layout)
        list_layout.addLayout(skill_layout)
        
        main_layout.addLayout(list_layout)

        # ボタンの初期状態を設定
        self._update_button_states()

        # 初期データの読み込み
        self._load_initial_data()

    def _update_button_states(self):
        """ボタンの有効/無効状態を更新する"""
        has_group = bool(self.category_group_combo.currentText())
        has_category = bool(self.parent_list.currentItem())
        has_skill = bool(self.child_list.currentItem())
        
        # グループ関連
        self.edit_group_btn.setEnabled(has_group)
        self.delete_group_btn.setEnabled(has_group)
        
        # カテゴリー関連
        self.add_parent_btn.setEnabled(has_group)
        self.edit_parent_btn.setEnabled(has_category)
        self.delete_parent_btn.setEnabled(has_category)
        
        # スキル関連
        self.add_child_btn.setEnabled(has_category)
        self.edit_child_btn.setEnabled(has_skill)
        self.delete_child_btn.setEnabled(has_skill)

    def _connect_signals(self):
        """シグナルを接続する"""
        # グループ関連
        self.category_group_combo.currentIndexChanged.connect(self._on_group_selected)
        self.category_group_combo.currentIndexChanged.connect(self._update_button_states)
        self.add_group_btn.clicked.connect(self._on_add_group)
        self.edit_group_btn.clicked.connect(self._on_edit_group)
        self.delete_group_btn.clicked.connect(self._on_delete_group)
        
        # カテゴリー関連
        self.parent_list.currentRowChanged.connect(self._on_parent_selected)
        self.parent_list.currentRowChanged.connect(self._update_button_states)
        self.add_parent_btn.clicked.connect(self._on_add_category)
        self.edit_parent_btn.clicked.connect(self._on_edit_category)
        self.delete_parent_btn.clicked.connect(self._on_delete_category)
        
        # スキル関連
        self.child_list.currentRowChanged.connect(self._update_button_states)
        self.add_child_btn.clicked.connect(self._on_add_skill)
        self.edit_child_btn.clicked.connect(self._on_edit_skill)
        self.delete_child_btn.clicked.connect(self._on_delete_skill)
