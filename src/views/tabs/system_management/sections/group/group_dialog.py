from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox
)

class GroupDialog(QDialog):
    def __init__(self, parent=None, group_data=None):
        super().__init__(parent)
        self.group_data = group_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('グループ' + ('の編集' if self.group_data else 'の追加'))
        layout = QVBoxLayout(self)
        
        # 名前入力
        name_layout = QHBoxLayout()
        name_label = QLabel("グループ名:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # 説明入力
        desc_layout = QVBoxLayout()
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        
        # ボタン
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('キャンセル')
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(name_layout)
        layout.addLayout(desc_layout)
        layout.addLayout(button_layout)
        
        # イベントの接続
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # 既存データの設定
        if self.group_data:
            self.name_edit.setText(self.group_data['name'])
            self.desc_edit.setText(self.group_data.get('description', ''))

    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip()
        }

    def accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, '警告', 'グループ名を入力してください。')
            return
        super().accept()
