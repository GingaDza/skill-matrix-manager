from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from typing import Optional, Any

class LeftPane(QWidget):
    """左ペインコンポーネント"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing LeftPane")
        
        super().__init__()
        self._setup_ui()
        self._setup_signals()

    def _setup_ui(self):
        """UIコンポーネントの設定"""
        self.logger.debug("Setting up LeftPane UI")
        
        # メインレイアウト
        layout = QVBoxLayout()
        
        # グループ選択部分
        group_layout = QHBoxLayout()
        self.group_combo = QComboBox()
        self.add_group_button = QPushButton("追加")
        self.remove_group_button = QPushButton("削除")
        
        group_layout.addWidget(self.group_combo)
        group_layout.addWidget(self.add_group_button)
        group_layout.addWidget(self.remove_group_button)
        
        # ユーザーリスト部分
        self.user_list = QListWidget()
        
        # ユーザー操作ボタン
        user_button_layout = QHBoxLayout()
        self.add_user_button = QPushButton("追加")
        self.remove_user_button = QPushButton("削除")
        
        user_button_layout.addWidget(self.add_user_button)
        user_button_layout.addWidget(self.remove_user_button)
        
        # レイアウトの組み立て
        layout.addLayout(group_layout)
        layout.addWidget(self.user_list)
        layout.addLayout(user_button_layout)
        
        self.setLayout(layout)
        self.logger.debug("LeftPane UI setup completed")

    def _setup_signals(self):
        """内部シグナルの設定"""
        self.logger.debug("Connecting LeftPane signals")
        
        # ボタンの有効/無効の初期設定
        self.remove_group_button.setEnabled(False)
        self.add_user_button.setEnabled(False)
        self.remove_user_button.setEnabled(False)
        
        # グループ選択変更時の処理
        self.group_combo.currentIndexChanged.connect(
            self._on_group_selection_changed
        )
        
        # ユーザー選択変更時の処理
        self.user_list.itemSelectionChanged.connect(
            self._on_user_selection_changed
        )
        
        self.logger.debug("LeftPane signals connected")

    def connect_signals(self, handler):
        """外部シグナルの接続"""
        self.logger.debug("Connecting external signals")
        
        # グループ操作
        self.add_group_button.clicked.connect(handler.on_add_group)
        self.remove_group_button.clicked.connect(handler.on_remove_group)
        self.group_combo.currentIndexChanged.connect(handler.on_group_changed)
        
        # ユーザー操作
        self.add_user_button.clicked.connect(handler.on_add_user)
        self.remove_user_button.clicked.connect(handler.on_remove_user)
        
        self.logger.debug("External signals connected")

    def _on_group_selection_changed(self, index: int):
        """グループ選択変更時の処理"""
        self.logger.debug(f"Group selection changed to index {index}")
        
        # ボタンの有効/無効を設定
        has_selection = index >= 0
        self.remove_group_button.setEnabled(has_selection)
        self.add_user_button.setEnabled(has_selection)
        
        # ユーザーリストの選択をクリア
        self.user_list.clearSelection()
        self.remove_user_button.setEnabled(False)

    def _on_user_selection_changed(self):
        """ユーザー選択変更時の処理"""
        self.logger.debug("User selection changed")
        
        # 削除ボタンの有効/無効を設定
        has_selection = len(self.user_list.selectedItems()) > 0
        self.remove_user_button.setEnabled(has_selection)

    def get_selected_group_id(self) -> Optional[int]:
        """選択されているグループIDを取得"""
        return self.group_combo.currentData()

    def get_selected_user_id(self) -> Optional[int]:
        """選択されているユーザーIDを取得"""
        items = self.user_list.selectedItems()
        if not items:
            return None
        return items[0].data(Qt.ItemDataRole.UserRole)

    def update_button_states(self):
        """ボタンの状態を更新"""
        # グループ関連
        group_selected = self.group_combo.currentIndex() >= 0
        self.remove_group_button.setEnabled(group_selected)
        self.add_user_button.setEnabled(group_selected)
        
        # ユーザー関連
        user_selected = len(self.user_list.selectedItems()) > 0
        self.remove_user_button.setEnabled(user_selected)
