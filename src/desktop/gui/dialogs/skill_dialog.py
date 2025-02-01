# src/desktop/gui/dialogs/skill_dialog.py
"""
Skill dialog implementation
Created: 2025-01-31 14:17:11
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox,
    QDialogButtonBox
)

class SkillDialog(QDialog):
    def __init__(self, data_manager, parent=None, skill=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.skill = skill
        self.setup_ui()
        
        if skill:
            self.setWindowTitle("スキル編集")
            self.load_skill_data()
        else:
            self.setWindowTitle("スキル追加")
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # フォーム
        form = QFormLayout()
        
        self.name_edit = QLineEdit()
        form.addRow("名前:", self.name_edit)
        
        self.category_combo = QComboBox()
        self.update_categories()
        form.addRow("カテゴリー:", self.category_combo)
        
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
    
    def update_categories(self):
        """カテゴリー一覧の更新"""
        self.category_combo.clear()
        
        for category in self.data_manager.get_group_categories():
            self.category_combo.addItem(category.name, category.id)
    
    def load_skill_data(self):
        """スキルデータの読み込み"""
        if self.skill:
            self.name_edit.setText(self.skill.name)
            self.description_edit.setText(self.skill.description)
            
            # カテゴリーの選択
            index = self.category_combo.findData(self.skill.category_id)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
    
    def get_skill_data(self):
        """スキルデータの取得"""
        return {
            'name': self.name_edit.text().strip(),
            'category_id': self.category_combo.currentData(),
            'description': self.description_edit.toPlainText().strip()
        }
    
    def accept(self):
        """OKボタン押下時の処理"""
        try:
            data = self.get_skill_data()
            
            if self.skill:
                # 既存スキルの更新
                self.skill.name = data['name']
                self.skill.category_id = data['category_id']
                self.skill.description = data['description']
                self.data_manager.skills_changed.emit()
            else:
                # 新規スキルの作成
                self.data_manager.create_skill(**data)
            
            super().accept()
            
        except ValueError as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "エラー", str(e))