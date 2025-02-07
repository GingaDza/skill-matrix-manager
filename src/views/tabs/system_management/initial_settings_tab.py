from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QSplitter
)
from PyQt6.QtCore import Qt
import logging

from ..base_tab import BaseTab
from ...components.lists.category_tree_widget import CategoryTreeWidget
from ...components.lists.group_list_widget import GroupListWidget

logger = logging.getLogger(__name__)

class InitialSettingsTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
        logger.debug("InitialSettingsTab initialized")

    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # メインスプリッター
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左側（グループリスト）
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_layout.addWidget(QLabel("グループ一覧"))
        self.group_list = GroupListWidget(self)
        left_layout.addWidget(self.group_list)
        
        # グループ操作ボタン
        group_buttons = QVBoxLayout()
        add_group_btn = QPushButton("グループ追加")
        edit_group_btn = QPushButton("グループ編集")
        delete_group_btn = QPushButton("グループ削除")
        
        add_group_btn.clicked.connect(self.add_group)
        edit_group_btn.clicked.connect(self.edit_group)
        delete_group_btn.clicked.connect(self.delete_group)
        
        group_buttons.addWidget(add_group_btn)
        group_buttons.addWidget(edit_group_btn)
        group_buttons.addWidget(delete_group_btn)
        left_layout.addLayout(group_buttons)
        
        # 右側（カテゴリーツリー）
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        right_layout.addWidget(QLabel("カテゴリーとスキル"))
        self.category_tree = CategoryTreeWidget(self)
        right_layout.addWidget(self.category_tree)
        
        # カテゴリー操作ボタン
        category_buttons = QHBoxLayout()
        add_category_btn = QPushButton("カテゴリー追加")
        edit_category_btn = QPushButton("カテゴリー編集")
        delete_category_btn = QPushButton("カテゴリー削除")
        add_skill_btn = QPushButton("スキル追加")
        
        add_category_btn.clicked.connect(self.add_category)
        edit_category_btn.clicked.connect(self.edit_category)
        delete_category_btn.clicked.connect(self.delete_category)
        add_skill_btn.clicked.connect(self.add_skill)
        
        category_buttons.addWidget(add_category_btn)
        category_buttons.addWidget(edit_category_btn)
        category_buttons.addWidget(delete_category_btn)
        category_buttons.addWidget(add_skill_btn)
        right_layout.addLayout(category_buttons)
        
        # 新規タブ追加ボタン
        add_tab_btn = QPushButton("新規タブ追加")
        add_tab_btn.clicked.connect(self.add_new_tab)
        right_layout.addWidget(add_tab_btn)
        
        # スプリッターに追加
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        layout.addWidget(splitter)
        
        logger.debug("InitialSettingsTab UI setup completed")

    def load_data(self):
        try:
            self.group_list.load_groups()
            self.category_tree.load_categories()
            logger.debug("InitialSettingsTab data loaded")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def add_group(self):
        from ...dialogs import GroupDialog
        try:
            dialog = GroupDialog(self)
            if dialog.exec():
                name = dialog.get_name()
                if name:
                    self.parent.db.add_group(name)
                    self.group_list.load_groups()
                    logger.debug(f"Added group: {name}")
        except Exception as e:
            logger.error(f"Error adding group: {str(e)}")
            self.show_error("グループの追加に失敗しました")

    def edit_group(self):
        from ...dialogs import GroupDialog
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                self.show_warning("編集するグループを選択してください")
                return

            dialog = GroupDialog(self, current_item.text())
            if dialog.exec():
                new_name = dialog.get_name()
                if new_name:
                    self.parent.db.update_group(current_item.item_id, new_name)
                    self.group_list.load_groups()
                    logger.debug(f"Updated group to: {new_name}")
        except Exception as e:
            logger.error(f"Error editing group: {str(e)}")
            self.show_error("グループの編集に失敗しました")

    def delete_group(self):
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                self.show_warning("削除するグループを選択してください")
                return

            if self.confirm_delete(f"グループ '{current_item.text()}' を削除してもよろしいですか？"):
                self.parent.db.delete_group(current_item.item_id)
                self.group_list.load_groups()
                logger.debug(f"Deleted group: {current_item.text()}")
        except Exception as e:
            logger.error(f"Error deleting group: {str(e)}")
            self.show_error("グループの削除に失敗しました")

    def add_category(self):
        from ...dialogs import CategoryDialog
        try:
            dialog = CategoryDialog(self)
            if dialog.exec():
                name = dialog.get_name()
                if name:
                    category_id = self.parent.db.add_category(name)
                    self.category_tree.load_categories()
                    self.parent.add_category_tab(name, category_id)
                    logger.debug(f"Added category: {name}")
        except Exception as e:
            logger.error(f"Error adding category: {str(e)}")
            self.show_error("カテゴリーの追加に失敗しました")

    def edit_category(self):
        from ...dialogs import CategoryDialog
        try:
            current_item = self.category_tree.currentItem()
            if not current_item or current_item.parent():
                self.show_warning("編集するカテゴリーを選択してください")
                return

            dialog = CategoryDialog(self, current_item.text(0))
            if dialog.exec():
                new_name = dialog.get_name()
                if new_name:
                    self.parent.db.update_category(current_item.item_id, new_name)
                    self.category_tree.load_categories()
                    logger.debug(f"Updated category to: {new_name}")
        except Exception as e:
            logger.error(f"Error editing category: {str(e)}")
            self.show_error("カテゴリーの編集に失敗しました")

    def delete_category(self):
        try:
            current_item = self.category_tree.currentItem()
            if not current_item or current_item.parent():
                self.show_warning("削除するカテゴリーを選択してください")
                return

            if self.confirm_delete(f"カテゴリー '{current_item.text(0)}' を削除してもよろしいですか？"):
                self.parent.db.delete_category(current_item.item_id)
                self.category_tree.load_categories()
                logger.debug(f"Deleted category: {current_item.text(0)}")
        except Exception as e:
            logger.error(f"Error deleting category: {str(e)}")
            self.show_error("カテゴリーの削除に失敗しました")

    def add_skill(self):
        from ...dialogs import SkillDialog
        try:
            current_item = self.category_tree.currentItem()
            if not current_item:
                self.show_warning("スキルを追加するカテゴリーを選択してください")
                return

            category_item = current_item if not current_item.parent() else current_item.parent()
            dialog = SkillDialog(self)
            if dialog.exec():
                name, description = dialog.get_data()
                if name:
                    self.parent.db.add_skill(name, category_item.item_id, description)
                    self.category_tree.load_categories()
                    logger.debug(f"Added skill: {name}")
        except Exception as e:
            logger.error(f"Error adding skill: {str(e)}")
            self.show_error("スキルの追加に失敗しました")

    def add_new_tab(self):
        try:
            current_item = self.category_tree.currentItem()
            if not current_item:
                self.show_warning("タブを追加するカテゴリーを選択してください")
                return

            category_item = current_item if not current_item.parent() else current_item.parent()
            self.parent.add_category_tab(category_item.text(0), category_item.item_id)
            logger.debug(f"Added new tab for category: {category_item.text(0)}")
        except Exception as e:
            logger.error(f"Error adding new tab: {str(e)}")
            self.show_error("新規タブの追加に失敗しました")
