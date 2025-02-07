# src/views/tabs/system_management/group_manager.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QMessageBox
)
from .base_classes import ListItemWithId, AddEditDialog
import logging

logger = logging.getLogger(__name__)

class GroupManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        logger.debug("GroupManager initialized")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # タイトル
        layout.addWidget(QLabel("グループ管理"))
        
        # グループリスト
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # ボタンレイアウト
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("追加")
        edit_btn = QPushButton("編集")
        delete_btn = QPushButton("削除")
        
        add_btn.clicked.connect(self.add_group)
        edit_btn.clicked.connect(self.edit_group)
        delete_btn.clicked.connect(self.delete_group)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)
        
        logger.debug("GroupManager UI setup completed")

    def load_groups(self):
        try:
            groups = self.parent.db.get_all_groups()
            self.group_list.clear()
            for group_id, name, _ in groups:
                self.group_list.addItem(ListItemWithId(name, group_id))
            logger.debug(f"Loaded {len(groups)} groups")
        except Exception as e:
            logger.error(f"Error loading groups: {str(e)}")
            raise

    def add_group(self):
        try:
            dialog = AddEditDialog(self, "グループ追加")
            if dialog.exec():
                name = dialog.get_name()
                if name:
                    group_id = self.parent.db.add_group(name)
                    self.group_list.addItem(ListItemWithId(name, group_id))
                    self.parent.emit_group_update()
                    logger.debug(f"Added group: {name} (ID: {group_id})")
        except Exception as e:
            logger.error(f"Error adding group: {str(e)}")
            QMessageBox.critical(self, "エラー", str(e))

    def edit_group(self):
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "編集するグループを選択してください。")
                return

            dialog = AddEditDialog(self, "グループ編集", current_item.text())
            if dialog.exec():
                new_name = dialog.get_name()
                if new_name:
                    self.parent.db.update_group(current_item.item_id, new_name)
                    current_item.setText(new_name)
                    self.parent.emit_group_update()
                    logger.debug(f"Edited group to: {new_name}")
        except Exception as e:
            logger.error(f"Error editing group: {str(e)}")
            QMessageBox.critical(self, "エラー", str(e))

    def delete_group(self):
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "削除するグループを選択してください。")
                return

            reply = QMessageBox.question(
                self, '確認', 
                f'グループ "{current_item.text()}" を削除してもよろしいですか？\n'
                f'※所属するユーザーも削除されます',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.parent.db.delete_group(current_item.item_id)
                self.group_list.takeItem(self.group_list.row(current_item))
                self.parent.emit_group_update()
                logger.debug(f"Deleted group: {current_item.text()}")
        except Exception as e:
            logger.error(f"Error deleting group: {str(e)}")
            QMessageBox.critical(self, "エラー", str(e))