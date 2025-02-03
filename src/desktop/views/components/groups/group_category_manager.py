# src/desktop/views/components/groups/group_category_manager.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from ....controllers.group_controller import GroupController
from ....controllers.category_controller import CategoryController
from ....utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class GroupCategoryManager(QWidget):
    """グループとカテゴリーの関連付けを管理するウィジェット"""
    
    def __init__(self, group_controller: GroupController, category_controller: CategoryController):
        """
        初期化
        Args:
            group_controller: グループコントローラー
            category_controller: カテゴリーコントローラー
        """
        super().__init__()
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        self.group_controller = group_controller
        self.category_controller = category_controller
        self.current_group_id = None
        
        self.setup_ui()
        
        logger.debug(f"{self.current_time} - GroupCategoryManager initialized")

    def setup_ui(self):
        """UIのセットアップ"""
        try:
            layout = QVBoxLayout(self)
            
            # カテゴリーツリー
            self.tree = QTreeWidget()
            self.tree.setHeaderLabels(["Category", "Description"])
            self.tree.itemChanged.connect(self.on_item_changed)
            layout.addWidget(self.tree)
            
            # ボタンレイアウト
            button_layout = QHBoxLayout()
            
            # 全選択ボタン
            select_all_button = QPushButton("Select All")
            select_all_button.clicked.connect(self.select_all)
            button_layout.addWidget(select_all_button)
            
            # 全解除ボタン
            deselect_all_button = QPushButton("Deselect All")
            deselect_all_button.clicked.connect(self.deselect_all)
            button_layout.addWidget(deselect_all_button)
            
            layout.addLayout(button_layout)
            
            logger.debug(f"{self.current_time} - GroupCategoryManager UI setup completed")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup GroupCategoryManager UI: {str(e)}")
            raise

    def set_current_group(self, group_id: int):
        """
        現在のグループを設定
        
        Args:
            group_id: グループID
        """
        try:
            self.current_group_id = group_id
            self.refresh_categories()
            logger.debug(f"{self.current_time} - Set current group: {group_id}")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to set current group: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to set current group: {str(e)}"
            )

    def refresh_categories(self):
        """カテゴリーツリーを更新"""
        try:
            if self.current_group_id is None:
                return
                
            self.tree.clear()
            
            # 全てのカテゴリーを取得
            categories = self.category_controller.get_all_categories()
            
            # グループに関連付けられたカテゴリーを取得
            group_categories = self.group_controller.get_group_categories(self.current_group_id)
            group_category_ids = {c.id for c in group_categories}
            
            # カテゴリーをIDでインデックス化
            category_dict = {category.id: category for category in categories}
            
            # ルートカテゴリーとサブカテゴリーを整理
            root_categories = []
            child_categories = {}
            
            for category in categories:
                if category.parent_id is None:
                    root_categories.append(category)
                else:
                    if category.parent_id not in child_categories:
                        child_categories[category.parent_id] = []
                    child_categories[category.parent_id].append(category)
            
            # ツリーを構築
            for root_category in sorted(root_categories, key=lambda x: x.name):
                root_item = self._create_tree_item(root_category, root_category.id in group_category_ids)
                self.tree.addTopLevelItem(root_item)
                self._add_child_categories(root_item, root_category.id, child_categories, group_category_ids)
            
            logger.debug(f"{self.current_time} - Refreshed categories for group {self.current_group_id}")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to refresh categories: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to refresh categories: {str(e)}"
            )

    def _create_tree_item(self, category, is_selected: bool) -> QTreeWidgetItem:
        """
        カテゴリー用のツリーアイテムを作成
        
        Args:
            category: カテゴリーオブジェクト
            is_selected: 選択状態
            
        Returns:
            QTreeWidgetItem: 作成されたツリーアイテム
        """
        item = QTreeWidgetItem([category.name, category.description or ""])
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(0, Qt.CheckState.Checked if is_selected else Qt.CheckState.Unchecked)
        return item

    def _add_child_categories(self, parent_item: QTreeWidgetItem, parent_id: int, child_categories: dict, selected_categories: set):
        """
        再帰的に子カテゴリーを追加
        
        Args:
            parent_item: 親カテゴリーのツリーアイテム
            parent_id: 親カテゴリーID
            child_categories: 子カテゴリーの辞書
            selected_categories: 選択されているカテゴリーIDのセット
        """
        if parent_id in child_categories:
            for child in sorted(child_categories[parent_id], key=lambda x: x.name):
                child_item = self._create_tree_item(child, child.id in selected_categories)
                parent_item.addChild(child_item)
                self._add_child_categories(child_item, child.id, child_categories, selected_categories)

    def on_item_changed(self, item: QTreeWidgetItem, column: int):
        """
        アイテムの状態が変更された時のハンドラー
        
        Args:
            item: 変更されたアイテム
            column: 変更された列
        """
        try:
            if self.current_group_id is None or column != 0:
                return
                
            category_id = item.data(0, Qt.ItemDataRole.UserRole)
            is_checked = item.checkState(0) == Qt.CheckState.Checked
            
            if is_checked:
                self.group_controller.add_category_to_group(self.current_group_id, category_id)
                logger.debug(f"{self.current_time} - Added category {category_id} to group {self.current_group_id}")
            else:
                self.group_controller.remove_category_from_group(self.current_group_id, category_id)
                logger.debug(f"{self.current_time} - Removed category {category_id} from group {self.current_group_id}")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update group categories: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to update group categories: {str(e)}"
            )

    def select_all(self):
        """全てのカテゴリーを選択"""
        try:
            if self.current_group_id is None:
                return
                
            self._set_all_check_states(Qt.CheckState.Checked)
            logger.debug(f"{self.current_time} - Selected all categories for group {self.current_group_id}")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to select all categories: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to select all categories: {str(e)}"
            )

    def deselect_all(self):
        """全てのカテゴリーの選択を解除"""
        try:
            if self.current_group_id is None:
                return
                
            self._set_all_check_states(Qt.CheckState.Unchecked)
            logger.debug(f"{self.current_time} - Deselected all categories for group {self.current_group_id}")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to deselect all categories: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to deselect all categories: {str(e)}"
            )

    def _set_all_check_states(self, state: Qt.CheckState):
        """
        全てのアイテムのチェック状態を設定
        
        Args:
            state: 設定する状態
        """
        def set_item_state(item: QTreeWidgetItem):
            item.setCheckState(0, state)
            for i in range(item.childCount()):
                set_item_state(item.child(i))
        
        for i in range(self.tree.topLevelItemCount()):
            set_item_state(self.tree.topLevelItem(i))