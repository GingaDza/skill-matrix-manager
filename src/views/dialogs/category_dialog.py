"""カテゴリーダイアログの実装"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QComboBox
)

class CategoryDialog(QDialog):
    """カテゴリーダイアログクラス"""

    def __init__(self, parent=None, current_name="", categories=None):
        super().__init__(parent)
        self.name = current_name
        self.parent_category = ""
        self._init_ui(current_name, categories or [])

    def _init_ui(self, current_name, categories):
        """UIの初期化"""
        self.setWindowTitle("カテゴリーの編集" if current_name else "カテゴリーの追加")
        layout = QVBoxLayout()

        # 名前入力
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("カテゴリー名:"))
        self.name_input = QLineEdit(current_name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # 親カテゴリー選択
        parent_layout = QHBoxLayout()
        parent_layout.addWidget(QLabel("親カテゴリー:"))
        self.parent_combo = QComboBox()
        self.parent_combo.addItem("なし")
        self.parent_combo.addItems(categories)
        parent_layout.addWidget(self.parent_combo)
        layout.addLayout(parent_layout)

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
        self.parent_category = self.parent_combo.currentText()
        if self.parent_category == "なし":
            self.parent_category = ""
        if self.name:
            super().accept()
