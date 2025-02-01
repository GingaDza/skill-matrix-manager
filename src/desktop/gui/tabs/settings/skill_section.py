# src/desktop/gui/tabs/settings/skill_section.py
"""
Skill settings section implementation
Created: 2025-01-31 13:18:57
Author: GingaDza
"""
from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
                             QFormLayout, QLineEdit, QTextEdit, 
                             QPushButton, QTreeWidget, QTreeWidgetItem,
                             QSpinBox)
from .section_base import SettingsSectionBase

class SkillSection(SettingsSectionBase):
    def setup_ui(self):
        super().setup_ui()
        
        self.group_box = QGroupBox("スキル設定")
        skill_layout = QVBoxLayout()
        
        # スキル追加フォーム
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        self.max_level = QSpinBox()
        self.max_level.setRange(1, 10)
        self.max_level.setValue(5)
        form.addRow("スキル名:", self.name_edit)
        form.addRow("説明:", self.desc_edit)
        form.addRow("最大レベル:", self.max_level)
        
        # ボタン
        buttons = QHBoxLayout()
        self.add_btn = QPushButton("スキル追加")
        self.edit_btn = QPushButton("スキル編集")
        self.delete_btn = QPushButton("スキル削除")
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.edit_btn)
        buttons.addWidget(self.delete_btn)
        
        # ツリーウィジェット
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["スキル名", "説明", "最大レベル"])
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 300)
        
        skill_layout.addLayout(form)
        skill_layout.addLayout(buttons)
        skill_layout.addWidget(self.tree)
        self.group_box.setLayout(skill_layout)
        
        self.layout.addWidget(self.group_box)
    
    def setup_signals(self):
        self.add_btn.clicked.connect(self.add_skill)
        self.edit_btn.clicked.connect(self.edit_skill)
        self.delete_btn.clicked.connect(self.delete_skill)
        self.tree.itemSelectionChanged.connect(self.skill_selected)
        
        # データマネージャーのシグナル
        self.data_manager.skills_changed.connect(self.update_display)
    
    def clear_inputs(self):
        self.name_edit.clear()
        self.desc_edit.clear()
        self.max_level.setValue(5)
    
    def update_display(self, category_id: str = None):
        """特定のカテゴリーのスキルを表示"""
        self.tree.clear()
        
        if category_id:
            skills = self.data_manager.get_category_skills(category_id)
            for skill in skills:
                item = QTreeWidgetItem([
                    skill.name,
                    skill.description or "",
                    str(skill.max_level)
                ])
                self.tree.addTopLevelItem(item)
    
    def add_skill(self):
        name = self.name_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        max_level = self.max_level.value()
        
        # 現在選択されているカテゴリーIDを取得する必要があります
        # これは親ウィジェットから提供される必要があります
        category_id = self.parent().get_selected_category_id()
        
        if name and category_id:
            self.data_manager.create_skill(name, category_id, description, max_level)
            self.clear_inputs()
    
    def edit_skill(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        name = self.name_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        max_level = self.max_level.value()
        
        if name:
            for skill in self.data_manager.skills.values():
                if skill.name == item.text(0):
                    skill.name = name
                    skill.description = description
                    skill.max_level = max_level
                    self.data_manager.skills_changed.emit()
                    break
            
            self.clear_inputs()
    
    def delete_skill(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        skill_to_delete = None
        
        for skill_id, skill in self.data_manager.skills.items():
            if skill.name == item.text(0):
                skill_to_delete = skill_id
                break
        
        if skill_to_delete:
            # カテゴリーからスキルを削除
            skill = self.data_manager.skills[skill_to_delete]
            if skill.category_id in self.data_manager.categories:
                category = self.data_manager.categories[skill.category_id]
                category.skills.remove(skill_to_delete)
            
            del self.data_manager.skills[skill_to_delete]
            self.data_manager.skills_changed.emit()
            self.clear_inputs()
    
    def skill_selected(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        self.name_edit.setText(item.text(0))
        self.desc_edit.setText(item.text(1))
        self.max_level.setValue(int(item.text(2)))