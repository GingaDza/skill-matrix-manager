# src/desktop/gui/tabs/settings/category_section.py
"""
Category settings section implementation
Created: 2025-01-31 13:18:57
Author: GingaDza
"""
from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
                             QFormLayout, QLineEdit, QTextEdit, 
                             QPushButton, QTreeWidget, QTreeWidgetItem)
from .section_base import SettingsSectionBase
from ...widgets.group_selector import GroupSelector

class CategorySection(SettingsSectionBase):
    def setup_ui(self):
        super().setup_ui()
        
        # グループセレクター
        self.group_selector = GroupSelector(self.data_manager)
        self.layout.addWidget(self.group_selector)
        
        self.group_box = QGroupBox("カテゴリー設定")
        category_layout = QVBoxLayout()
        
        # カテゴリー追加フォーム
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        form.addRow("カテゴリー名:", self.name_edit)
        form.addRow("説明:", self.desc_edit)
        
        # ボタン
        buttons = QHBoxLayout()
        self.add_btn = QPushButton("カテゴリー追加")
        self.edit_btn = QPushButton("カテゴリー編集")
        self.delete_btn = QPushButton("カテゴリー削除")
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.edit_btn)
        buttons.addWidget(self.delete_btn)
        
        # ツリーウィジェット
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["カテゴリー名", "説明", "スキル数"])
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 300)
        
        category_layout.addLayout(form)
        category_layout.addLayout(buttons)
        category_layout.addWidget(self.tree)
        self.group_box.setLayout(category_layout)
        
        self.layout.addWidget(self.group_box)
    
    def setup_signals(self):
        self.add_btn.clicked.connect(self.add_category)
        self.edit_btn.clicked.connect(self.edit_category)
        self.delete_btn.clicked.connect(self.delete_category)
        self.tree.itemSelectionChanged.connect(self.category_selected)
        
        # グループセレクターの変更シグナル
        self.group_selector.combo.currentIndexChanged.connect(self.update_display)
        
        # データマネージャーのシグナル
        self.data_manager.categories_changed.connect(self.update_display)
    
    def clear_inputs(self):
        self.name_edit.clear()
        self.desc_edit.clear()
    
    def update_display(self):
        self.tree.clear()
        
        selected_group_id = self.group_selector.combo.currentData()
        categories = self.data_manager.get_group_categories(selected_group_id)
        
        for category in categories:
            item = QTreeWidgetItem([
                category.name,
                category.description or "",
                str(len(category.skills))
            ])
            self.tree.addTopLevelItem(item)
    
    def add_category(self):
        name = self.name_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        selected_group_id = self.group_selector.combo.currentData()
        
        if name and selected_group_id:
            self.data_manager.create_category(name, selected_group_id, description)
            self.clear_inputs()
    
    def edit_category(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        name = self.name_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        
        if name:
            for category in self.data_manager.categories.values():
                if category.name == item.text(0):
                    category.name = name
                    category.description = description
                    self.data_manager.categories_changed.emit()
                    break
            
            self.clear_inputs()
    
    def delete_category(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        category_to_delete = None
        
        for category_id, category in self.data_manager.categories.items():
            if category.name == item.text(0):
                category_to_delete = category_id
                break
        
        if category_to_delete:
            # グループからカテゴリーを削除
            category = self.data_manager.categories[category_to_delete]
            if category.group_id in self.data_manager.groups:
                group = self.data_manager.groups[category.group_id]
                group.categories.remove(category_to_delete)
            
            del self.data_manager.categories[category_to_delete]
            self.data_manager.categories_changed.emit()
            self.clear_inputs()
    
    def category_selected(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        self.name_edit.setText(item.text(0))
        self.desc_edit.setText(item.text(1))