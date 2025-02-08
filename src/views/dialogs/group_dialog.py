"""グループダイアログの実装"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)

class GroupDialog(QDialog):
    """グループダイアログクラス"""

    def __init__(self, parent=None, current_name=""):
        super().__init__(parent)
        self.name = current_name
        self._init_ui(current_name)

    def _init_ui(self, current_name):
        """UIの初期化"""
        self.setWindowTitle("グループの編集" if current_name else "グループの追加")
        layout = QVBoxLayout()

        # 名前入力
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("グループ名:"))
        self.name_input = QLineEdit(current_name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

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
        if self.name:
            super().accept()
