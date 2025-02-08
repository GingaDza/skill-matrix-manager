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

class PlaceholderListWidget(QFrame):
    """プレースホルダー付きリストウィジェット"""
    
    def __init__(self, placeholder_text: str, parent: Optional[QWidget] = None):
        """
        初期化
        
        Args:
            placeholder_text (str): プレースホルダーのテキスト
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(200)  # 最小幅を設定
        self.list_widget.setMinimumHeight(300)  # 最小高さを設定
        
        self.placeholder_label = QLabel(placeholder_text)
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setStyleSheet("""
            QLabel {
                color: #666;
                padding: 10px;
                border: 1px dashed #999;
                border-radius: 4px;
                background: #f5f5f5;
                font-size: 12px;
            }
        """)
        
        layout.addWidget(self.list_widget)
        layout.addWidget(self.placeholder_label)
        
        self._update_placeholder_visibility()
        self.list_widget.model().rowsInserted.connect(self._update_placeholder_visibility)
        self.list_widget.model().rowsRemoved.connect(self._update_placeholder_visibility)

    def _update_placeholder_visibility(self):
        """プレースホルダーの表示/非表示を更新"""
        has_items = self.list_widget.count() > 0
        self.placeholder_label.setVisible(not has_items)
        self.list_widget.setVisible(has_items)

    def addItems(self, items):
        """アイテムを追加"""
        self.list_widget.addItems(items)

    def clear(self):
        """リストをクリア"""
        self.list_widget.clear()

    def currentItem(self):
        """現在選択されているアイテムを取得"""
        return self.list_widget.currentItem()

    def setCurrentRow(self, row: int):
        """指定した行を選択"""
        self.list_widget.setCurrentRow(row)

    def currentRowChanged(self, handler):
        """行選択変更時のシグナルを接続"""
        return self.list_widget.currentRowChanged.connect(handler)

class SettingsWidgetBase(BaseWidget, GroupManagerMixin, CategoryManagerMixin, SkillManagerMixin):
    """設定ウィジェットの基本クラス"""
    
    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """初期化"""
        super().__init__(db_manager=db_manager, parent=parent)
        self.setup()
        self.logger.info("SettingsWidgetBase initialized")

    def init_ui(self):
        """UIを初期化する"""
        # メインレイアウト
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # グループ選択部分
        group_frame = QFrame()
        group_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        group_layout = QVBoxLayout(group_frame)
        group_layout.setContentsMargins(10, 10, 10, 10)
        group_layout.setSpacing(5)
        
        group_label = QLabel("グループ")
        group_label.setFont(QFont("", weight=QFont.Weight.Bold))
        group_controls = QHBoxLayout()
        
        self.category_group_combo = QComboBox()
        self.category_group_combo.setPlaceholderText("グループを選択してください")
        self.category_group_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        
        button_style = """
            QPushButton {
                min-width: 60px;
                padding: 5px;
            }
        """
        
        self.add_group_btn = QPushButton("追加")
        self.add_group_btn.setStyleSheet(button_style)
        self.edit_group_btn = QPushButton("編集")
        self.edit_group_btn.setStyleSheet(button_style)
        self.delete_group_btn = QPushButton("削除")
        self.delete_group_btn.setStyleSheet(button_style)
        
        group_controls.addWidget(self.category_group_combo)
        group_controls.addWidget(self.add_group_btn)
        group_controls.addWidget(self.edit_group_btn)
        group_controls.addWidget(self.delete_group_btn)
        
        group_layout.addWidget(group_label)
        group_layout.addLayout(group_controls)
        main_layout.addWidget(group_frame)

        # カテゴリーとスキルのリスト部分
        lists_frame = QFrame()
        lists_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        list_layout = QHBoxLayout(lists_frame)
        list_layout.setContentsMargins(10, 10, 10, 10)
        list_layout.setSpacing(10)
        
        # カテゴリー部分
        category_layout = QVBoxLayout()
        category_label = QLabel("カテゴリー")
        category_label.setFont(QFont("", weight=QFont.Weight.Bold))
        self.parent_list = PlaceholderListWidget("グループを選択してください")
        
        category_btn_layout = QHBoxLayout()
        self.add_parent_btn = QPushButton("追加")
        self.add_parent_btn.setStyleSheet(button_style)
        self.edit_parent_btn = QPushButton("編集")
        self.edit_parent_btn.setStyleSheet(button_style)
        self.delete_parent_btn = QPushButton("削除")
        self.delete_parent_btn.setStyleSheet(button_style)
        
        category_btn_layout.addWidget(self.add_parent_btn)
        category_btn_layout.addWidget(self.edit_parent_btn)
        category_btn_layout.addWidget(self.delete_parent_btn)
        
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.parent_list)
        category_layout.addLayout(category_btn_layout)
        
        # スキル部分
        skill_layout = QVBoxLayout()
        skill_label = QLabel("スキル")
        skill_label.setFont(QFont("", weight=QFont.Weight.Bold))
        self.child_list = PlaceholderListWidget("カテゴリーを選択してください")
        
        skill_btn_layout = QHBoxLayout()
        self.add_child_btn = QPushButton("追加")
        self.add_child_btn.setStyleSheet(button_style)
        self.edit_child_btn = QPushButton("編集")
        self.edit_child_btn.setStyleSheet(button_style)
        self.delete_child_btn = QPushButton("削除")
        self.delete_child_btn.setStyleSheet(button_style)
        
        skill_btn_layout.addWidget(self.add_child_btn)
        skill_btn_layout.addWidget(self.edit_child_btn)
        skill_btn_layout.addWidget(self.delete_child_btn)
        
        skill_layout.addWidget(skill_label)
        skill_layout.addWidget(self.child_list)
        skill_layout.addLayout(skill_btn_layout)
        
        list_layout.addLayout(category_layout)
        list_layout.addLayout(skill_layout)
        
        main_layout.addWidget(lists_frame)

        # ボタンの初期状態を設定
        self._update_button_states()

        # 初期データの読み込み
        self._load_initial_data()