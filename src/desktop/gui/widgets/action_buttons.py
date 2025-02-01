# src/desktop/gui/widgets/action_buttons.py
"""
Action buttons widget
Created: 2025-01-31 13:11:12
Author: GingaDza
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ActionButtons(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.add_user_btn = QPushButton("ユーザー追加")
        self.edit_user_btn = QPushButton("ユーザー編集")
        self.delete_user_btn = QPushButton("ユーザー削除")
        self.export_btn = QPushButton("データ出力")
        
        layout.addWidget(self.add_user_btn)
        layout.addWidget(self.edit_user_btn)
        layout.addWidget(self.delete_user_btn)
        layout.addWidget(self.export_btn)
        layout.addStretch()