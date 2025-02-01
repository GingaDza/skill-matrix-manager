# src/desktop/gui/tabs/settings/group_section.py
"""
Group settings section implementation
Created: 2025-01-31 13:16:31
Author: GingaDza
"""
from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
                             QFormLayout, QLineEdit, QTextEdit, 
                             QPushButton, QTreeWidget, QTreeWidgetItem)
from .section_base import SettingsSectionBase

class GroupSection(SettingsSectionBase):
    def setup_ui(self):
        super().setup_ui()
        
        self.group_box = QGroupBox("グループ設定")
        group_layout = QVBoxLayout()
        
        # グループ追加フォーム
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        form.addRow("グループ名:", self.name_edit)
        form.addRow("説明:", self.desc_edit)
        
        # ボタン
        buttons = QHBoxLayout()
        self.add_btn = QPushButton("グループ追加")
        self.edit_btn = QPushButton("グループ編集")
        self.delete_btn = QPushButton("グループ削除")
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.edit_btn)
        buttons.addWidget(self.delete_btn)
        
        # ツリーウィジェット
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["グループ名", "説明", "所属人数"])
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 300)
        
        group_layout.addLayout(form)
        group_layout.addLayout(buttons)
        group_layout.addWidget(self.tree)
        self.group_box.setLayout(group_layout)
        
        self.layout.addWidget(self.group_box)
    
    def setup_signals(self):
        self.add_btn.clicked.connect(self.add_group)
        self.edit_btn.clicked.connect(self.edit_group)
        self.delete_btn.clicked.connect(self.delete_group)
        self.tree.itemSelectionChanged.connect(self.group_selected)
        
        # データマネージャーのシグナル
        self.data_manager.groups_changed.connect(self.update_display)
    
    def clear_inputs(self):
        self.name_edit.clear()
        self.desc_edit.clear()
    
    def update_display(self):
        self.tree.clear()
        for group in self.data_manager.groups.values():
            item = QTreeWidgetItem([
                group.name,
                group.description or "",
                str(len(group.members))
            ])
            self.tree.addTopLevelItem(item)
    
    def add_group(self):
        name = self.name_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        
        if name:
            self.data_manager.create_group(name, description)
            self.clear_inputs()
    
    def edit_group(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        name = self.name_edit.text().strip()
        description = self.desc_edit.toPlainText().strip()
        
        if name:
            for group in self.data_manager.groups.values():
                if group.name == item.text(0):
                    group.name = name
                    group.description = description
                    self.data_manager.groups_changed.emit()
                    break
            
            self.clear_inputs()
    
    def delete_group(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        for group_id, group in self.data_manager.groups.items():
            if group.name == item.text(0):
                del self.data_manager.groups[group_id]
                self.data_manager.groups_changed.emit()
                break
        
        self.clear_inputs()
    
    def group_selected(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        self.name_edit.setText(item.text(0))
        self.desc_edit.setText(item.text(1))