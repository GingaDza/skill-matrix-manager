"""ダイアログの実装"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QSpinBox, QFormLayout
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

class EditSkillDialog(QDialog):
    """スキル編集ダイアログ"""

    def __init__(self, parent=None, current_name="", current_description="",
                current_min_level=1, current_max_level=5):
        super().__init__(parent)
        self.name = current_name
        self.description = current_description
        self.min_level = current_min_level
        self.max_level = current_max_level
        self._init_ui(current_name, current_description,
                     current_min_level, current_max_level)

    def _init_ui(self, current_name, current_description,
                current_min_level, current_max_level):
        """UIの初期化"""
        self.setWindowTitle("スキルの編集")
        layout = QFormLayout()

        # 名前入力
        self.name_input = QLineEdit(current_name)
        layout.addRow("名前:", self.name_input)

        # 説明入力
        self.description_input = QLineEdit(current_description)
        layout.addRow("説明:", self.description_input)

        # レベル範囲入力
        self.min_level_input = QSpinBox()
        self.min_level_input.setRange(1, 5)
        self.min_level_input.setValue(current_min_level)
        layout.addRow("最小レベル:", self.min_level_input)

        self.max_level_input = QSpinBox()
        self.max_level_input.setRange(1, 5)
        self.max_level_input.setValue(current_max_level)
        layout.addRow("最大レベル:", self.max_level_input)

        # ボタン
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("キャンセル")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addRow("", button_layout)

        self.setLayout(layout)

    def accept(self):
        """OKボタンが押された時の処理"""
        self.name = self.name_input.text().strip()
        self.description = self.description_input.text().strip()
        self.min_level = self.min_level_input.value()
        self.max_level = self.max_level_input.value()

        if not self.name:
            return

        if self.min_level > self.max_level:
            self.min_level = self.max_level

        super().accept()
