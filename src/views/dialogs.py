"""ダイアログの実装"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)

class AddUserDialog(QDialog):
    """ユーザー追加ダイアログ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.name = ""
        self.email = ""
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        self.setWindowTitle("ユーザーの追加")
        layout = QVBoxLayout()

        # 名前入力
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("名前:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # メール入力
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("メール:"))
        self.email_input = QLineEdit()
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        # ボタン
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        """OKボタンが押された時の処理"""
        self.name = self.name_input.text().strip()
        self.email = self.email_input.text().strip()
        if self.name:
            super().accept()

class EditUserDialog(AddUserDialog):
    """ユーザー編集ダイアログ"""

    def __init__(self, parent=None, current_name=""):
        super().__init__(parent)
        self.setWindowTitle("ユーザーの編集")
        self.name_input.setText(current_name)
