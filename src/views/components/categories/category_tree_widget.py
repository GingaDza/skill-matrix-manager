# src/desktop/views/components/categories/category_tree_widget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from ....controllers.category_controller import CategoryController
from ....utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class CategoryTreeWidget(QWidget):
    """カテゴリーツリーウィジェット"""
    
    category_selected = pyqtSignal(int)  # カテゴリー選択時のシグナル
    
    def __init__(self, category_controller: CategoryController):
        """
        初期化
        Args:
            category_controller: カテゴリーコントローラー
        """
        super().__init__()
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        self.category_controller = category_controller
        self.setup_ui()
        self.refresh_categories()
        
        logger.debug(f"{self.current_time} - CategoryTreeWidget initialized")

    def setup_ui(self):
        """UIのセットアップ"""
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # ツリーウィジェット
            self.tree = QTreeWidget()
            self.tree.setHeaderLabels(["Category", "Description"])
            self.tree.itemSelectionChanged.connect(self.on_selection_changed)
            layout.addWidget(self.tree)
            
            # ボタンレイアウト
            button_layout = QHBoxLayout()
            
            # 追加ボタン
            add_button = QPushButton("Add Category")
            add_button.clicked.connect(self.add_category)
            button_layout.addWidget(add_button)
            
            # 編集ボタン
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(self.edit_category)
            button_layout.addWidget(edit_button)
            
            # 削除ボタン
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.delete_category)
            button_layout.addWidget(delete_button)
            
            layout.addLayout(button_layout)
            
            logger.debug(f"{self.current_time} - CategoryTreeWidget UI setup completed")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup CategoryTreeWidget UI: {str(e)}")
            raise

    def add_category(self):
        """新しいカテゴリーを追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "Add Category",
                "Enter category name:"
            )
            
            if ok and name:
                description, ok = QInputDialog.getText(
                    self,
                    "Add Category",
                    "Enter category description (optional):"
                )
                
                if ok:  # キャンセルされなかった場合
                    # 親カテゴリーのIDを取得（選択されている場合）
                    parent_id = None
                    current_item = self.tree.currentItem()
                    if current_item:
                        parent_id = current_item.data(0, Qt.ItemDataRole.UserRole)
                    
                    category_id = self.category_controller.create_category(
                        name=name,
                        description=description,
                        parent_id=parent_id
                    )
                    self.refresh_categories()
                    logger.debug(f"{self.current_time} - Added new category: {name} (ID: {category_id})")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to add category: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to add category: {str(e)}"
            )

    # src/desktop/views/components/categories/category_tree_widget.py の edit_category メソッド
    def edit_category(self):
        """選択されたカテゴリーを編集"""
        try:
            current_item = self.tree.currentItem()
            if not current_item:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please select a category to edit"
                )
                return
                
            category_id = current_item.data(0, Qt.ItemDataRole.UserRole)
            category = self.category_controller.get_category(category_id)  # get_category_by_id から get_category に変更
            
            name, ok = QInputDialog.getText(
                self,
                "Edit Category",
                "Enter new category name:",
                text=category.name
            )
            
            if ok and name:
                description, ok = QInputDialog.getText(
                    self,
                    "Edit Category",
                    "Enter new category description (optional):",
                    text=category.description or ""
                )
                
                if ok:  # キャンセルされなかった場合
                    success = self.category_controller.update_category(
                        category_id=category_id,
                        name=name,
                        description=description
                    )
                    
                    if success:
                        self.refresh_categories()
                        logger.debug(f"{self.current_time} - Updated category: {name} (ID: {category_id})")
                    else:
                        QMessageBox.warning(
                            self,
                            "Warning",
                            f"Failed to update category {name}"
                        )
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to edit category: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to edit category: {str(e)}"
            )

    def delete_category(self):
        """選択されたカテゴリーを削除"""
        try:
            current_item = self.tree.currentItem()
            if not current_item:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please select a category to delete"
                )
                return
                
            category_id = current_item.data(0, Qt.ItemDataRole.UserRole)
            category = self.category_controller.get_category(category_id)  # get_category_by_id から get_category に変更
            
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete the category '{category.name}'?\n"
                "This will also remove all subcategories.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.category_controller.delete_category(category_id)
                if success:
                    self.refresh_categories()
                    logger.debug(f"{self.current_time} - Deleted category: {category.name} (ID: {category_id})")
                else:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        f"Failed to delete category {category.name}"
                    )
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete category: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to delete category: {str(e)}"
            )

    def refresh_categories(self):
        """カテゴリーツリーを更新"""
        try:
            self.tree.clear()
            categories = self.category_controller.get_all_categories()
            
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
                root_item = self._create_tree_item(root_category)
                self.tree.addTopLevelItem(root_item)
                self._add_child_categories(root_item, root_category.id, child_categories)
            
            logger.debug(f"{self.current_time} - Refreshed category tree with {len(categories)} categories")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to refresh categories: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to refresh categories: {str(e)}"
            )

    def _create_tree_item(self, category) -> QTreeWidgetItem:
        """
        カテゴリー用のツリーアイテムを作成
        
        Args:
            category: カテゴリーオブジェクト
            
        Returns:
            QTreeWidgetItem: 作成されたツリーアイテム
        """
        item = QTreeWidgetItem([category.name, category.description or ""])
        item.setData(0, Qt.ItemDataRole.UserRole, category.id)
        return item

    def _add_child_categories(self, parent_item: QTreeWidgetItem, parent_id: int, child_categories: dict):
        """
        再帰的に子カテゴリーを追加
        
        Args:
            parent_item: 親カテゴリーのツリーアイテム
            parent_id: 親カテゴリーID
            child_categories: 子カテゴリーの辞書
        """
        if parent_id in child_categories:
            for child in sorted(child_categories[parent_id], key=lambda x: x.name):
                child_item = self._create_tree_item(child)
                parent_item.addChild(child_item)
                self._add_child_categories(child_item, child.id, child_categories)

    def on_selection_changed(self):
        """カテゴリー選択時のハンドラー"""
        try:
            current_item = self.tree.currentItem()
            if current_item:
                category_id = current_item.data(0, Qt.ItemDataRole.UserRole)
                self.category_selected.emit(category_id)
                logger.debug(f"{self.current_time} - Category selected: {current_item.text(0)} (ID: {category_id})")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to handle category selection: {str(e)}")