from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QPushButton,
    QListWidget, QDialog, QMessageBox
)
from .....dialogs.input_dialog import InputDialog
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GroupSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("グループリスト", parent)
        self.current_time = datetime(2025, 2, 3, 10, 44, 41)
        self.current_user = "GingaDza"
        
        logger.debug(f"{self.current_time} - {self.current_user} GroupSection initialization started")
        self.groups = []
        self.setup_ui()
        logger.debug(f"{self.current_time} - {self.current_user} GroupSection initialization completed")
    
    def setup_ui(self):
        logger.debug(f"{self.current_time} - {self.current_user} Setting up GroupSection UI")
        layout = QVBoxLayout()
        
        # グループリスト
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # ボタン群
        self.setup_buttons(layout)
        
        self.setLayout(layout)
        logger.debug(f"{self.current_time} - {self.current_user} GroupSection UI setup completed")

    def setup_buttons(self, layout):
        """ボタンの設定"""
        logger.debug(f"{self.current_time} - {self.current_user} Setting up buttons")
        
        # ボタンの作成
        self.add_btn = QPushButton("グループ追加")
        self.edit_btn = QPushButton("グループ編集")
        self.delete_btn = QPushButton("グループ削除")
        
        # ボタンの有効/無効状態を設定
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        
        # シグナル接続前のデバッグ出力
        logger.debug(f"Add button is enabled: {self.add_btn.isEnabled()}")
        
        # シグナル接続
        self.add_btn.clicked.connect(self.add_group)
        logger.debug(f"{self.current_time} - {self.current_user} Add button signal connected")
        
        self.edit_btn.clicked.connect(self.edit_group)
        logger.debug(f"{self.current_time} - {self.current_user} Edit button signal connected")
        
        self.delete_btn.clicked.connect(self.delete_group)
        logger.debug(f"{self.current_time} - {self.current_user} Delete button signal connected")
        
        # リスト選択変更時のシグナル接続
        self.group_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        # ボタンの追加
        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        logger.debug(f"{self.current_time} - {self.current_user} Buttons setup completed")

    def add_group(self):
        """グループを追加"""
        logger.debug(f"{self.current_time} - {self.current_user} Add group button clicked")
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Creating InputDialog")
            dialog = InputDialog("グループ追加", "グループ名:", parent=self)
            logger.debug(f"{self.current_time} - {self.current_user} InputDialog created")
            
            result = dialog.exec()
            logger.debug(f"{self.current_time} - {self.current_user} Dialog result: {result}")
            
            if result == QDialog.DialogCode.Accepted:
                name = dialog.get_input()
                logger.debug(f"{self.current_time} - {self.current_user} Input received: {name}")
                
                if self.validate_input(name):
                    self.groups.append(name)
                    self.group_list.addItem(name)
                    logger.info(f"{self.current_time} - {self.current_user} Group added: {name}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in add_group: {str(e)}")
            logger.exception("Detailed traceback:")
            self.show_error(f"グループの追加に失敗しました。\nエラー: {str(e)}")

    def edit_group(self):
        """グループを編集"""
        logger.debug(f"{self.current_time} - {self.current_user} Edit group button clicked")
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                self.show_error("編集するグループを選択してください。")
                return
            
            old_name = current_item.text()
            logger.debug(f"{self.current_time} - {self.current_user} Creating InputDialog for editing {old_name}")
            dialog = InputDialog("グループ編集", "新しいグループ名:", old_name, self)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_name = dialog.get_input()
                logger.debug(f"{self.current_time} - {self.current_user} New name input: {new_name}")
                
                if self.validate_input(new_name, exclude=old_name):
                    idx = self.groups.index(old_name)
                    self.groups[idx] = new_name
                    current_item.setText(new_name)
                    logger.info(f"{self.current_time} - {self.current_user} Group edited: {old_name} -> {new_name}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in edit_group: {str(e)}")
            logger.exception("Detailed traceback:")
            self.show_error("グループの編集に失敗しました。")

    def delete_group(self):
        """グループを削除"""
        logger.debug(f"{self.current_time} - {self.current_user} Delete group button clicked")
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                self.show_error("削除するグループを選択してください。")
                return
            
            name = current_item.text()
            logger.debug(f"{self.current_time} - {self.current_user} Attempting to delete group: {name}")
            
            if self.show_confirmation(f"グループ '{name}' を削除しますか？"):
                self.groups.remove(name)
                self.group_list.takeItem(self.group_list.row(current_item))
                logger.info(f"{self.current_time} - {self.current_user} Group deleted: {name}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in delete_group: {str(e)}")
            logger.exception("Detailed traceback:")
            self.show_error("グループの削除に失敗しました。")

    def on_selection_changed(self):
        """リストの選択が変更されたときの処理"""
        has_selection = bool(self.group_list.currentItem())
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        logger.debug(f"{self.current_time} - {self.current_user} Selection changed, buttons enabled: {has_selection}")

    def validate_input(self, name, exclude=None):
        """入力値の検証"""
        name = name.strip()
        if not name:
            self.show_error("グループ名を入力してください。")
            return False
        if name in self.groups and name != exclude:
            self.show_error("このグループ名は既に存在します。")
            return False
        return True

    def show_error(self, message):
        """エラーメッセージを表示"""
        logger.debug(f"{self.current_time} - {self.current_user} Showing error: {message}")
        QMessageBox.critical(self, "エラー", message)

    def show_confirmation(self, message):
        """確認ダイアログを表示"""
        logger.debug(f"{self.current_time} - {self.current_user} Showing confirmation: {message}")
        return QMessageBox.question(
            self, "確認", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes

    def get_selected_group(self):
        """選択されているグループを取得"""
        item = self.group_list.currentItem()
        return item.text() if item else None