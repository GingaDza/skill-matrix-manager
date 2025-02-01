# src/desktop/gui/dialogs/category_dialog.py
"""
Category dialog implementation
Created: 2025-01-31 14:17:11
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QDialogButtonBox
)

class CategoryDialog(QDialog):
    def __init__(self, data_manager, parent=None, category=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.category = category
        self.setup_ui()
        
        if category:
            self.setWindowTitle("カテゴリー編集")
            self.load_category_data()
        else:
            self.setWindowTitle("カテゴリー追加")
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # フォーム
        form = QFormLayout()
        
        self.name_edit = QLineEdit()
        form.addRow("名前:", self.name_edit)
        
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
    
    def load_category_data(self):
        """カテゴリーデータの読み込み"""
        if self.category:
            self.name_edit.setText(self.category.name)
            self.description_edit.setText(self.category.description)
    
    def get_category_data(self):
        """カテゴリーデータの取得"""
        return {
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip()
        }
    
    def accept(self):
        """OKボタン押下時の処理"""
        try:
            data = self.get_category_data()
            
            if self.category:
                # 既存カテゴリーの更新
                self.category.name = data['name']
                self.category.description = data['description']
                self.data_manager.categories_changed.emit()
            else:
                # 新規カテゴリーの作成
                self.data_manager.create_category(**data)
            
            super().accept()
            
        except ValueError as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "エラー", str(e))