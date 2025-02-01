# src/desktop/gui/dialogs/user_dialog.py
"""
User dialog implementation
Created: 2025-01-31 14:24:55
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QDialogButtonBox
)

class UserDialog(QDialog):
    def __init__(self, data_manager, parent=None, user=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.user = user
        self.setup_ui()
        
        if user:
            self.setWindowTitle("ユーザー編集")
            self.load_user_data()
        else:
            self.setWindowTitle("ユーザー追加")
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # フォーム
        form = QFormLayout()
        
        self.name_edit = QLineEdit()
        form.addRow("名前:", self.name_edit)
        
        self.email_edit = QLineEdit()
        form.addRow("メールアドレス:", self.email_edit)
        
        self.group_combo = QComboBox()
        self.update_groups()
        form.addRow("グループ:", self.group_combo)
        
        layout.addLayout(form)
        
        # ボタン
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def update_groups(self):
        """グループ一覧の更新"""
        self.group_combo.clear()
        self.group_combo.addItem("-- グループなし --", None)
        
        for group in self.data_manager.groups.values():
            self.group_combo.addItem(group.name, group.id)
    
    def load_user_data(self):
        """ユーザーデータの読み込み"""
        if self.user:
            self.name_edit.setText(self.user.name)
            self.email_edit.setText(self.user.email)
            
            # グループの選択
            index = self.group_combo.findData(self.user.group_id)
            if index >= 0:
                self.group_combo.setCurrentIndex(index)
    
    def get_user_data(self):
        """ユーザーデータの取得"""
        return {
            'name': self.name_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'group_id': self.group_combo.currentData()
        }
    
    def accept(self):
        """OKボタン押下時の処理"""
        try:
            data = self.get_user_data()
            
            if self.user:
                # 既存ユーザーの更新
                self.user.name = data['name']
                self.user.email = data['email']
                self.data_manager.update_user_group(
                    self.user.id,
                    data['group_id']
                )
            else:
                # 新規ユーザーの作成
                self.data_manager.create_user(**data)
            
            super().accept()
            
        except ValueError as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "エラー", str(e))