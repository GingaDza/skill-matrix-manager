from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QPushButton,
    QListWidget, QMessageBox
)
from desktop.views.dialogs.input_dialog import InputDialog
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GroupSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("グループリスト", parent)
        self.current_time = datetime(2025, 2, 3, 10, 7, 0)
        self.current_user = "GingaDza"
        
        self.groups = []
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # グループリスト
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # ボタン群
        self.add_button = QPushButton("グループ追加")
        self.edit_button = QPushButton("グループ編集")
        self.delete_button = QPushButton("グループ削除")
        
        self.add_button.clicked.connect(self.add_group)
        self.edit_button.clicked.connect(self.edit_group)
        self.delete_button.clicked.connect(self.delete_group)
        
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
    
    def add_group(self):
        dialog = InputDialog("グループ追加", "グループ名:")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_input()
            if self.validate_input(name):
                self.groups.append(name)
                self.group_list.addItem(name)
                logger.info(f"{self.current_time} - {self.current_user} added group: {name}")

    def get_selected_group(self):
        return self.group_list.currentItem()

    def validate_input(self, name):
        if not name:
            self.show_error("グループ名を入力してください。")
            return False
        if name in self.groups:
            self.show_error("このグループ名は既に存在します。")
            return False
        return True

    def show_error(self, message):
        QMessageBox.critical(self, "エラー", message)