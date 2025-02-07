# src/desktop/views/components/groups/group_list_widget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from ....controllers.group_controller import GroupController
from ....utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class GroupListWidget(QWidget):
    """グループリストウィジェット"""
    
    group_selected = pyqtSignal(int)  # グループ選択時のシグナル
    
    def __init__(self, group_controller: GroupController):
        """
        初期化
        Args:
            group_controller: グループコントローラー
        """
        super().__init__()
        self.current_time = TimeProvider.get_current_time()
        self.current_user = TimeProvider.get_current_user()
        
        self.group_controller = group_controller
        self.setup_ui()
        self.refresh_groups()
        
        logger.debug(f"{self.current_time} - GroupListWidget initialized")

    def setup_ui(self):
        """UIのセットアップ"""
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # リストウィジェット
            self.list = QListWidget()
            self.list.itemSelectionChanged.connect(self.on_selection_changed)
            layout.addWidget(self.list)
            
            # ボタンレイアウト
            button_layout = QHBoxLayout()
            
            # 追加ボタン
            add_button = QPushButton("Add Group")
            add_button.clicked.connect(self.add_group)
            button_layout.addWidget(add_button)
            
            # 編集ボタン
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(self.edit_group)
            button_layout.addWidget(edit_button)
            
            # 削除ボタン
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.delete_group)
            button_layout.addWidget(delete_button)
            
            layout.addLayout(button_layout)
            
            logger.debug(f"{self.current_time} - GroupListWidget UI setup completed")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup GroupListWidget UI: {str(e)}")
            raise

    def add_group(self):
        """新しいグループを追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "Add Group",
                "Enter group name:"
            )
            
            if ok and name:
                description, ok = QInputDialog.getText(
                    self,
                    "Add Group",
                    "Enter group description (optional):"
                )
                
                if ok:  # キャンセルされなかった場合
                    group_id = self.group_controller.create_group(
                        name=name,
                        description=description
                    )
                    self.refresh_groups()
                    logger.debug(f"{self.current_time} - Added new group: {name} (ID: {group_id})")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to add group: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to add group: {str(e)}"
            )

    def edit_group(self):
        """選択されたグループを編集"""
        try:
            current_item = self.list.currentItem()
            if not current_item:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please select a group to edit"
                )
                return
                
            group_id = current_item.data(Qt.ItemDataRole.UserRole)
            group = self.group_controller.get_group(group_id)  # get_group_by_id から get_group に変更
        
            
            if not group:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Group with ID {group_id} not found"
                )
                return
                
            name, ok = QInputDialog.getText(
                self,
                "Edit Group",
                "Enter new group name:",
                text=group.name
            )
            
            if ok and name:
                description, ok = QInputDialog.getText(
                    self,
                    "Edit Group",
                    "Enter new group description (optional):",
                    text=group.description or ""
                )
                
                if ok:  # キャンセルされなかった場合
                    success = self.group_controller.update_group(
                        group_id=group_id,
                        name=name,
                        description=description
                    )
                    
                    if success:
                        self.refresh_groups()
                        logger.debug(f"{self.current_time} - Updated group: {name} (ID: {group_id})")
                    else:
                        QMessageBox.warning(
                            self,
                            "Warning",
                            f"Failed to update group {name}"
                        )
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to edit group: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to edit group: {str(e)}"
            )

    def delete_group(self):
        """選択されたグループを削除"""
        try:
            current_item = self.list.currentItem()
            if not current_item:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Please select a group to delete"
                )
                return
                
            group_id = current_item.data(Qt.ItemDataRole.UserRole)
            group = self.group_controller.get_group(group_id)  # get_group_by_id から get_group に変更
        
            
            if not group:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Group with ID {group_id} not found"
                )
                return
                
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete the group '{group.name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.group_controller.delete_group(group_id)
                if success:
                    self.refresh_groups()
                    logger.debug(f"{self.current_time} - Deleted group: {group.name} (ID: {group_id})")
                else:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        f"Failed to delete group {group.name}"
                    )
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete group: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to delete group: {str(e)}"
            )

    def refresh_groups(self):
        """グループリストを更新"""
        try:
            self.list.clear()
            groups = self.group_controller.get_all_groups()
            
            for group in groups:
                item = QListWidgetItem(group.name)
                item.setData(Qt.ItemDataRole.UserRole, group.id)
                if group.description:
                    item.setToolTip(group.description)
                self.list.addItem(item)
                
            logger.debug(f"{self.current_time} - Refreshed group list with {len(groups)} groups")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to refresh groups: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to refresh groups: {str(e)}"
            )

    def on_selection_changed(self):
        """グループ選択時のハンドラー"""
        try:
            current_item = self.list.currentItem()
            if current_item:
                group_id = current_item.data(Qt.ItemDataRole.UserRole)
                self.group_selected.emit(group_id)
                logger.debug(f"{self.current_time} - Group selected: {current_item.text()} (ID: {group_id})")
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to handle group selection: {str(e)}")