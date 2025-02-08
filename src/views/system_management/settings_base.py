"""設定ウィジェットの基本クラス"""
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QListWidget,
    QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..base.base_widget import BaseWidget
from .group_manager import GroupManagerMixin
from .category_manager import CategoryManagerMixin
from .skill_manager import SkillManagerMixin

class ButtonStateManagerMixin:
    """ボタンの状態管理機能を提供するミックスイン"""
    
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

# ... (PlaceholderListWidgetクラスは変更なし)

class SettingsWidgetBase(BaseWidget, ButtonStateManagerMixin, GroupManagerMixin, CategoryManagerMixin, SkillManagerMixin):
    """設定ウィジェットの基本クラス"""
    
    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """初期化"""
        super().__init__(db_manager=db_manager, parent=parent)
        self.setup()
        self.logger.info("SettingsWidgetBase initialized")

    def _connect_signals(self):
        """シグナルを接続する"""
        # グループ関連
        self.category_group_combo.currentIndexChanged.connect(self._on_group_selected)
        self.category_group_combo.currentIndexChanged.connect(self._update_button_states)
        self.add_group_btn.clicked.connect(self._on_add_group)
        self.edit_group_btn.clicked.connect(self._on_edit_group)
        self.delete_group_btn.clicked.connect(self._on_delete_group)
        
        # カテゴリー関連
        self.parent_list.currentRowChanged(self._on_parent_selected)
        self.parent_list.currentRowChanged(self._update_button_states)
        self.add_parent_btn.clicked.connect(self._on_add_category)
        self.edit_parent_btn.clicked.connect(self._on_edit_category)
        self.delete_parent_btn.clicked.connect(self._on_delete_category)
        
        # スキル関連
        self.child_list.currentRowChanged(self._update_button_states)
        self.add_child_btn.clicked.connect(self._on_add_skill)
        self.edit_child_btn.clicked.connect(self._on_edit_skill)
        self.delete_child_btn.clicked.connect(self._on_delete_skill)

    # ... (init_uiメソッドは変更なし)