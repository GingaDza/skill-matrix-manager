from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from src.desktop.utils.time_utils import TimeProvider
from src.desktop.views.dialogs.group_dialog import GroupDialog

logger = logging.getLogger(__name__)

class GroupManagementWidget(QWidget):
    def __init__(self, group_controller, parent=None):
        super().__init__(parent)
        self.group_controller = group_controller
        self.current_time = TimeProvider.get_current_time()
        
        self.init_ui()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            layout = QVBoxLayout(self)
            
            # ボタンエリア
            button_layout = QHBoxLayout()
            self.add_button = QPushButton("追加")
            self.edit_button = QPushButton("編集")
            self.delete_button = QPushButton("削除")
            
            button_layout.addWidget(self.add_button)
            button_layout.addWidget(self.edit_button)
            button_layout.addWidget(self.delete_button)
            button_layout.addStretch()
            
            layout.addLayout(button_layout)
            
            # テーブル
            self.table = QTableWidget()
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["ID", "グループ名", "所属人数"])
            
            # テーブルのカスタマイズ
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            
            layout.addWidget(self.table)
            
            # シグナル/スロット接続
            self.add_button.clicked.connect(self.on_add_clicked)
            self.edit_button.clicked.connect(self.on_edit_clicked)
            self.delete_button.clicked.connect(self.on_delete_clicked)
            
            logger.debug(f"{self.current_time} - GroupManagementWidget UI initialized")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to initialize GroupManagementWidget UI: {str(e)}")
            raise
            
    def load_data(self):
        """グループデータの読み込み"""
        try:
            groups = self.group_controller.get_all_groups()
            
            self.table.setRowCount(len(groups))
            for i, group in enumerate(groups):
                # グループID
                id_item = QTableWidgetItem(str(group.id))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 0, id_item)
                
                # グループ名
                name_item = QTableWidgetItem(group.name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 1, name_item)
                
                # 所属人数（実装予定）
                count_item = QTableWidgetItem("0")  # 仮の値
                count_item.setFlags(count_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 2, count_item)
                
            logger.debug(f"{self.current_time} - Loaded {len(groups)} groups")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load group data: {str(e)}")
            QMessageBox.critical(self, "エラー", "グループデータの読み込みに失敗しました。")
            
    def on_add_clicked(self):
        """グループ追加ボタンのクリックハンドラ"""
        try:
            dialog = GroupDialog(parent=self)
            if dialog.exec() == GroupDialog.DialogCode.Accepted:
                name = dialog.get_group_name()
                if name:
                    self.group_controller.create_group(name)
                    self.load_data()
                    logger.debug(f"{self.current_time} - Group added: {name}")
                    QMessageBox.information(self, "成功", "グループを追加しました。")
                    
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to add group: {str(e)}")
            QMessageBox.critical(self, "エラー", f"グループの追加に失敗しました: {str(e)}")
            
    def on_edit_clicked(self):
        """グループ編集ボタンのクリックハンドラ"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "警告", "編集するグループを選択してください。")
                return
                
            group_id = int(self.table.item(current_row, 0).text())
            current_name = self.table.item(current_row, 1).text()
            
            dialog = GroupDialog(name=current_name, parent=self)
            if dialog.exec() == GroupDialog.DialogCode.Accepted:
                new_name = dialog.get_group_name()
                if new_name and new_name != current_name:
                    self.group_controller.update_group(group_id, new_name)
                    self.load_data()
                    logger.debug(f"{self.current_time} - Group updated: {new_name}")
                    QMessageBox.information(self, "成功", "グループを更新しました。")
                    
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to edit group: {str(e)}")
            QMessageBox.critical(self, "エラー", f"グループの編集に失敗しました: {str(e)}")
            
    def on_delete_clicked(self):
        """グループ削除ボタンのクリックハンドラ"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "警告", "削除するグループを選択してください。")
                return
                
            group_id = int(self.table.item(current_row, 0).text())
            group_name = self.table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self,
                "確認",
                f"グループ「{group_name}」を削除しますか？\n所属するユーザーのグループ設定は解除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.group_controller.delete_group(group_id)
                self.load_data()
                logger.debug(f"{self.current_time} - Group deleted: {group_name}")
                QMessageBox.information(self, "成功", "グループを削除しました。")
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete group: {str(e)}")
            QMessageBox.critical(self, "エラー", f"グループの削除に失敗しました: {str(e)}")