from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from .sections.group_section import GroupSection
from .sections.category_section import CategorySection
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InitialSettingsTab(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.current_time = datetime(2025, 2, 3, 11, 58, 21)  # Updated time
        self.current_user = "GingaDza"  # Updated user
        self.controllers = controllers
        
        # グループと親カテゴリーの関連付けを保持する辞書
        self.group_categories = {}  # {group_name: {parent_category: [child_categories]}}
        
        logger.debug(f"{self.current_time} - {self.current_user} Initializing InitialSettingsTab")
        self.setup_ui()
        self.setup_connections()
        logger.debug(f"{self.current_time} - {self.current_user} initialized InitialSettingsTab")

    def setup_ui(self):
        try:
            layout = QVBoxLayout()  # Changed to not pass self
            
            # 水平レイアウト
            h_layout = QHBoxLayout()
            
            # グループセクション
            self.group_section = GroupSection(self)
            h_layout.addWidget(self.group_section)
            
            # カテゴリーセクション
            self.category_section = CategorySection(self)
            h_layout.addWidget(self.category_section)
            
            layout.addLayout(h_layout)
            
            # 新規タブ追加ボタン
            self.add_tab_button = QPushButton("新規タブ追加")
            self.add_tab_button.clicked.connect(self.on_create_new_tab)  # Fixed connection
            self.add_tab_button.setEnabled(False)
            layout.addWidget(self.add_tab_button)
            
            self.setLayout(layout)  # Set the layout to the widget
            logger.debug(f"{self.current_time} - {self.current_user} UI setup completed successfully")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in setup_ui: {str(e)}")
            raise

    def setup_connections(self):
        """シグナル/スロット接続の設定"""
        try:
            # グループ選択変更時の処理
            self.group_section.group_list.itemSelectionChanged.connect(self.on_group_selection_changed)
            
            # カテゴリー選択変更時の処理
            self.category_section.parent_list.itemSelectionChanged.connect(self.update_tab_button_state)
            self.category_section.child_list.itemSelectionChanged.connect(self.update_tab_button_state)
            logger.debug(f"{self.current_time} - {self.current_user} Connections setup completed")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in setup_connections: {str(e)}")
            raise

    def on_group_selection_changed(self):
        """グループ選択変更時の処理"""
        try:
            selected_group = self.group_section.get_selected_group()
            logger.debug(f"{self.current_time} - {self.current_user} Group selection changed to: {selected_group}")
            
            # カテゴリーセクションに選択されたグループを通知
            self.category_section.set_selected_group(selected_group)
            
            if selected_group:
                if selected_group not in self.group_categories:
                    self.group_categories[selected_group] = {}
                
                # カテゴリーセクションを更新
                self.category_section.clear_categories()
                
                # グループに関連付けられた親カテゴリーを表示
                for parent_cat in self.group_categories[selected_group]:
                    self.category_section.add_parent_category(parent_cat)
                    # 子カテゴリーも表示
                    for child_cat in self.group_categories[selected_group][parent_cat]:
                        self.category_section.add_child_category(parent_cat, child_cat)
                
                logger.debug(f"{self.current_time} - {self.current_user} Updated categories for group: {selected_group}")
                logger.debug(f"{self.current_time} - {self.current_user} Current group_categories: {self.group_categories}")
            
            self.update_tab_button_state()
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in group selection change: {str(e)}")
            logger.exception("Detailed traceback:")

    def update_tab_button_state(self):
        """タブ追加ボタンの状態を更新"""
        try:
            group_selected = self.group_section.get_selected_group() is not None
            category_selected = self.category_section.get_selected_category() is not None
            self.add_tab_button.setEnabled(group_selected and category_selected)
            logger.debug(f"{self.current_time} - {self.current_user} Tab button state updated: {group_selected and category_selected}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error updating tab button state: {str(e)}")

    def on_create_new_tab(self):
        """新規タブ作成ボタンがクリックされた時の処理"""
        try:
            group = self.group_section.get_selected_group()
            category = self.category_section.get_selected_category()
            
            if group and category:
                parent_category, child_category = category
                # TODO: 新規タブの作成処理を実装
                logger.info(f"{self.current_time} - {self.current_user} Creating new tab: {group}/{parent_category}/{child_category}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error creating new tab: {str(e)}")

    def add_category_to_group(self, group_name, parent_category):
        """グループに親カテゴリーを追加"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Adding category {parent_category} to group {group_name}")
            if group_name not in self.group_categories:
                self.group_categories[group_name] = {}
            
            if parent_category not in self.group_categories[group_name]:
                self.group_categories[group_name][parent_category] = []
                logger.debug(f"{self.current_time} - {self.current_user} Category added to group. Updated structure: {self.group_categories}")
                return True
            return False
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error adding category to group: {str(e)}")
            return False

    def add_child_category_to_group(self, group_name, parent_category, child_category):
        """グループの親カテゴリーに子カテゴリーを追加"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Adding child category {child_category} to parent {parent_category} in group {group_name}")
            if (group_name in self.group_categories and 
                parent_category in self.group_categories[group_name]):
                if child_category not in self.group_categories[group_name][parent_category]:
                    self.group_categories[group_name][parent_category].append(child_category)
                    logger.debug(f"{self.current_time} - {self.current_user} Child category added. Updated structure: {self.group_categories}")
                    return True
            return False
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error adding child category to group: {str(e)}")
            return False

    def get_all_data(self):
        """全てのデータを取得"""
        return {
            'group_categories': self.group_categories.copy()
        }