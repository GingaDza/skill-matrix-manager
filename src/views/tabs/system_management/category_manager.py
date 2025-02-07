# src/views/tabs/system_management/category_manager.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QMessageBox
)
from .base_classes import ListItemWithId, AddEditDialog
import logging

logger = logging.getLogger(__name__)

class CategoryManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        logger.debug("CategoryManager initialized")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # タイトル
        layout.addWidget(QLabel("カテゴリー管理"))
        
        # カテゴリーリスト
        self.category_list = QListWidget()
        layout.addWidget(self.category_list)
        
        # ボタンレイアウト
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("追加")
        edit_btn = QPushButton("編集")
        delete_btn = QPushButton("削除")
        
        add_btn.clicked.connect(self.add_category)
        edit_btn.clicked.connect(self.edit_category)
        delete_btn.clicked.connect(self.delete_category)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)
        
        logger.debug("CategoryManager UI setup completed")

    def load_categories(self):
        try:
            categories = self.parent.db.get_all_categories()
            self.category_list.clear()
            for category_id, name in categories:
                self.category_list.addItem(ListItemWithId(name, category_id))
            logger.debug(f"Loaded {len(categories)} categories")
        except Exception as e:
            logger.error(f"Error loading categories: {str(e)}")
            raise

    def add_category(self):
        try:
            dialog = AddEditDialog(self, "カテゴリー追加")
            if dialog.exec():
                name = dialog.get_name()
                if name:
                    category_id = self.parent.db.add_category(name)
                    self.category_list.addItem(ListItemWithId(name, category_id))
                    self.parent.category_added.emit(name)
                    logger.debug(f"Added category: {name} (ID: {category_id})")
        except Exception as e:
            logger.error(f"Error adding category: {str(e)}")
            QMessageBox.critical(self, "エラー", str(e))

    def edit_category(self):
        try:
            current_item = self.category_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "編集するカテゴリーを選択してください。")
                return

            dialog = AddEditDialog(self, "カテゴリー編集", current_item.text())
            if dialog.exec():
                new_name = dialog.get_name()
                if new_name:
                    self.parent.db.update_category(current_item.item_id, new_name)
                    current_item.setText(new_name)
                    logger.debug(f"Edited category to: {new_name}")
        except Exception as e:
            logger.error(f"Error editing category: {str(e)}")
            QMessageBox.critical(self, "エラー", str(e))

    def delete_category(self):
        try:
            current_item = self.category_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "削除するカテゴリーを選択してください。")
                return

            reply = QMessageBox.question(
                self, '確認', 
                f'カテゴリー "{current_item.text()}" を削除してもよろしいですか？\n'
                f'※このカテゴリーのスキルも削除されます',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.parent.db.delete_category(current_item.item_id)
                self.category_list.takeItem(self.category_list.row(current_item))
                logger.debug(f"Deleted category: {current_item.text()}")
        except Exception as e:
            logger.error(f"Error deleting category: {str(e)}")
            QMessageBox.critical(self, "エラー", str(e))