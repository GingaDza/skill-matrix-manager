from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QComboBox
)
from PyQt6.QtCore import pyqtSignal
import logging

class LeftPane(QWidget):
    """左ペインコンポーネント"""
    group_changed = pyqtSignal(int)
    add_user_clicked = pyqtSignal()
    edit_user_clicked = pyqtSignal()
    delete_user_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # グループ選択
        group_label = QLabel("グループ選択:")
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(
            lambda idx: self.group_changed.emit(idx)
        )

        # ユーザーリスト
        user_label = QLabel("ユーザー一覧:")
        self.user_list = QListWidget()

        # ボタン
        add_button = QPushButton("ユーザー追加")
        edit_button = QPushButton("ユーザー編集")
        delete_button = QPushButton("ユーザー削除")

        add_button.clicked.connect(self.add_user_clicked.emit)
        edit_button.clicked.connect(self.edit_user_clicked.emit)
        delete_button.clicked.connect(self.delete_user_clicked.emit)

        # レイアウトに追加
        layout.addWidget(group_label)
        layout.addWidget(self.group_combo)
        layout.addWidget(user_label)
        layout.addWidget(self.user_list)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.addStretch()

    def get_selected_user(self):
        """選択中のユーザー情報を取得"""
        return self.user_list.currentItem()

    def get_current_group_id(self):
        """現在選択中のグループIDを取得"""
        return self.group_combo.currentData()
