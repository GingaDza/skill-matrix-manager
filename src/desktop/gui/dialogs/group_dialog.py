# src/desktop/gui/dialogs/group_dialog.py
"""
Group dialog implementation
Created: 2025-01-31 21:57:46
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QDialogButtonBox,
    QMessageBox
)

class GroupDialog(QDialog):
    def __init__(self, data_manager, parent=None, group=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.group = group
        self.setup_ui()
        
        if group:
            self.setWindowTitle("グループ編集")
            self.load_group_data()
        else:
            self.setWindowTitle("グループ追加")
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # フォーム
        form = QFormLayout()
        
        self.name_edit = QLineEdit()
        form.addRow("グループ名:", self.name_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form.addRow("説明:", self.description_edit)
        
        layout.addLayout(form)
        
        # ボタン
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_group_data(self):
        """グループデータの読み込み"""
        if self.group:
            self.name_edit.setText(self.group.name)
            self.description_edit.setText(self.group.description)
    
    def get_group_data(self):
        """グループデータの取得"""
        return {
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip()
        }
    
# src/desktop/gui/dialogs/group_dialog.py の accept メソッドを修正

    def accept(self):
        """OKボタン押下時の処理"""
        try:
            data = self.get_group_data()
            
            if not data['name']:
                raise ValueError("グループ名は必須です")
            
            if self.group:
                # 既存グループの更新
                self.group.name = data['name']
                self.group.description = data['description']
                self.data_manager.groups_changed.emit()
            else:
                # 新規グループの作成
                self.data_manager.create_group(**data)
            
            super().accept()
            
        except ValueError as e:
            QMessageBox.warning(self, "エラー", str(e))