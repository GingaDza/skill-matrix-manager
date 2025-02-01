# src/desktop/gui/tabs/settings/settings_tab.py
"""
Main settings tab implementation
Created: 2025-01-31 13:21:35
Author: GingaDza
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from ....models.data_manager import DataManager
from .group_section import GroupSection
from .category_section import CategorySection
from .skill_section import SkillSection

class SettingsTab(QWidget):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.setup_ui()
    
    def setup_ui(self):
        # メインレイアウト
        main_layout = QVBoxLayout(self)
        
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        
        # スクロールの内容
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # 各セクションの追加
        self.group_section = GroupSection(self.data_manager)
        self.category_section = CategorySection(self.data_manager)
        self.skill_section = SkillSection(self.data_manager)
        
        content_layout.addWidget(self.group_section)
        content_layout.addWidget(self.category_section)
        content_layout.addWidget(self.skill_section)
        
        # スペーサーの追加
        content_layout.addStretch()
        
        # スクロールエリアにコンテンツを設定
        scroll.setWidget(content)
        
        # 初期表示の更新
        self.update_displays()
        
        # シグナル接続
        self.setup_signals()
    
    def setup_signals(self):
        # カテゴリー選択時のスキル表示更新
        self.category_section.tree.itemSelectionChanged.connect(self.update_skill_display)
    
    def update_displays(self):
        """全セクションの表示を更新"""
        self.group_section.update_display()
        self.category_section.update_display()
    
    def update_skill_display(self):
        """選択されたカテゴリーのスキルを表示"""
        selected_items = self.category_section.tree.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        # カテゴリーを探す
        category_id = None
        for cat_id, category in self.data_manager.categories.items():
            if category.name == item.text(0):
                category_id = cat_id
                break
        
        if category_id:
            self.skill_section.update_display(category_id)
    
    def get_selected_category_id(self) -> str:
        """現在選択されているカテゴリーのIDを取得"""
        selected_items = self.category_section.tree.selectedItems()
        if not selected_items:
            return None
        
        item = selected_items[0]
        for category_id, category in self.data_manager.categories.items():
            if category.name == item.text(0):
                return category_id
        
        return None