# src/desktop/gui/widgets/skill_matrix.py
"""
Skill matrix widget implementation
Created: 2025-01-31 22:12:30
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QTreeWidget, QTreeWidgetItem, QPushButton,
    QLabel, QHeaderView
)
from PySide6.QtCore import Qt

class SkillMatrixWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        self.setup_signals()
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # ヘッダー部分
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # タイトル
        title = QLabel("スキルマトリックス")
        title.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(title)
        
        # スペーサー
        header_layout.addStretch()
        
        # 新規カテゴリー追加ボタン
        self.add_category_btn = QPushButton("カテゴリー追加")
        self.add_category_btn.setMaximumWidth(120)
        header_layout.addWidget(self.add_category_btn)
        
        # 新規スキル追加ボタン
        self.add_skill_btn = QPushButton("スキル追加")
        self.add_skill_btn.setMaximumWidth(100)
        header_layout.addWidget(self.add_skill_btn)
        
        layout.addWidget(header)
        
        # スキルマトリックスツリー
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["カテゴリー/スキル"])
        self.tree.setColumnWidth(0, 300)
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        layout.addWidget(self.tree)
        
        # ステータス表示
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
    
    def setup_signals(self):
        """シグナル/スロット接続"""
        self.add_category_btn.clicked.connect(self.add_category)
        self.add_skill_btn.clicked.connect(self.add_skill)
        self.data_manager.categories_changed.connect(self.update_matrix)
        self.data_manager.skills_changed.connect(self.update_matrix)
        
        # 初期表示
        self.update_matrix()
    
    def update_matrix(self):
        """スキルマトリックスの更新"""
        self.tree.clear()
        
        # カテゴリーとスキルの表示
        for category in self.data_manager.get_group_categories():
            # カテゴリーアイテムの作成
            category_item = QTreeWidgetItem([category.name])
            category_item.setData(0, Qt.UserRole, category.id)
            category_item.setToolTip(0, category.description)
            self.tree.addTopLevelItem(category_item)
            
            # スキルの表示
            for skill in self.data_manager.get_category_skills(category.id):
                skill_item = QTreeWidgetItem([skill.name])
                skill_item.setData(0, Qt.UserRole, skill.id)
                skill_item.setToolTip(0, skill.description)
                category_item.addChild(skill_item)
            
            category_item.setExpanded(True)
        
        # ステータス更新
        self.update_status()
    
    def update_status(self):
        """ステータス更新"""
        category_count = self.tree.topLevelItemCount()
        skill_count = sum(
            self.tree.topLevelItem(i).childCount()
            for i in range(category_count)
        )
        self.status_label.setText(
            f"カテゴリー数: {category_count}, スキル数: {skill_count}"
        )
    
    def add_category(self):
        """新規カテゴリーの追加"""
        from ..dialogs.category_dialog import CategoryDialog
        dialog = CategoryDialog(self.data_manager, self)
        dialog.exec()
    
    def add_skill(self):
        """新規スキルの追加"""
        from ..dialogs.skill_dialog import SkillDialog
        dialog = SkillDialog(self.data_manager, self)
        dialog.exec()