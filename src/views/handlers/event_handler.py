from PyQt6.QtCore import QObject, Qt, pyqtSlot
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QWidget
import logging
from typing import Optional, Any

class SafeHandler:
    """安全なイベントハンドラーベース"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._db = None
        self._main_window = None
        self._data_handler = None
        
    def _initialize_refs(self, db: Any, main_window: QWidget, data_handler: Any):
        """参照の初期化"""
        self._db = db
        self._main_window = main_window
        self._data_handler = data_handler
        
    @property
    def db(self) -> Any:
        """データベース参照の取得"""
        return self._db
            
    @property
    def main_window(self) -> Optional[QWidget]:
        """メインウィンドウ参照の取得"""
        return self._main_window
            
    @property
    def data_handler(self) -> Any:
        """データハンドラー参照の取得"""
        return self._data_handler

    def cleanup(self):
        """リソースのクリーンアップ"""
        self._db = None
        self._main_window = None
        self._data_handler = None

class EventHandler(QObject, SafeHandler):
    """イベント処理ハンドラー"""
    
    def __init__(self, db: Any, main_window: QWidget, data_handler: Any):
        QObject.__init__(self)
        SafeHandler.__init__(self)
        self._initialize_refs(db, main_window, data_handler)
        self.logger.setLevel(logging.DEBUG)

    @pyqtSlot()
    def on_add_user(self):
        """ユーザー追加処理"""
        self.logger.debug("Starting user addition")
        
        try:
            if not self.main_window:
                self.logger.error("メインウィンドウが見つかりません")
                return
                
            left_pane = self.main_window.left_pane
            group_id = left_pane.get_selected_group_id()
            
            if group_id is None:
                self.logger.warning("No group selected for user addition")
                QMessageBox.warning(
                    self.main_window,
                    "警告",
                    "グループを選択してください。"
                )
                return
                
            name, ok = QInputDialog.getText(
                self.main_window,
                "ユーザー追加",
                "ユーザー名を入力してください："
            )
            
            if ok and name.strip():
                self.logger.debug(f"Adding user '{name}' to group {group_id}")
                self.db.add_user_to_group(name.strip(), group_id)
                self.logger.info(f"Successfully added user '{name}'")
                
                if self.data_handler:
                    self.data_handler.refresh_user_list()
                    
        except Exception as e:
            self.logger.error(f"Error adding user: {e}")
            if self.main_window:
                QMessageBox.critical(
                    self.main_window,
                    "エラー",
                    "ユーザーの追加に失敗しました。"
                )

    @pyqtSlot()
    def on_remove_user(self):
        """ユーザー削除処理"""
        self.logger.debug("Starting user removal")
        
        try:
            if not self.main_window:
                self.logger.error("メインウィンドウが見つかりません")
                return
                
            left_pane = self.main_window.left_pane
            user_id = left_pane.get_selected_user_id()
            
            if user_id is None:
                self.logger.warning("No user selected for removal")
                QMessageBox.warning(
                    self.main_window,
                    "警告",
                    "ユーザーを選択してください。"
                )
                return
                
            confirm = QMessageBox.question(
                self.main_window,
                "確認",
                "選択したユーザーを削除しますか？",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.logger.debug(f"Removing user {user_id}")
                self.db.remove_user(user_id)
                self.logger.info(f"Successfully removed user {user_id}")
                
                if self.data_handler:
                    self.data_handler.refresh_user_list()
                    
        except Exception as e:
            self.logger.error(f"Error removing user: {e}")
            if self.main_window:
                QMessageBox.critical(
                    self.main_window,
                    "エラー",
                    "ユーザーの削除に失敗しました。"
                )

    @pyqtSlot()
    def on_add_group(self):
        """グループ追加処理"""
        self.logger.debug("Starting group addition")
        
        try:
            if not self.main_window:
                self.logger.error("メインウィンドウが見つかりません")
                return
                
            name, ok = QInputDialog.getText(
                self.main_window,
                "グループ追加",
                "グループ名を入力してください："
            )
            
            if ok and name.strip():
                self.logger.debug(f"Adding group '{name}'")
                self.db.add_group(name.strip())
                self.logger.info(f"Successfully added group '{name}'")
                
                if self.data_handler:
                    self.data_handler.refresh_data()
                    
        except Exception as e:
            self.logger.error(f"Error adding group: {e}")
            if self.main_window:
                QMessageBox.critical(
                    self.main_window,
                    "エラー",
                    "グループの追加に失敗しました。"
                )

    @pyqtSlot()
    def on_remove_group(self):
        """グループ削除処理"""
        self.logger.debug("Starting group removal")
        
        try:
            if not self.main_window:
                self.logger.error("メインウィンドウが見つかりません")
                return
                
            left_pane = self.main_window.left_pane
            group_id = left_pane.get_selected_group_id()
            
            if group_id is None:
                self.logger.warning("No group selected for removal")
                QMessageBox.warning(
                    self.main_window,
                    "警告",
                    "グループを選択してください。"
                )
                return
                
            confirm = QMessageBox.question(
                self.main_window,
                "確認",
                "選択したグループを削除しますか？\n"
                "※所属するユーザーも全て削除されます。",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.logger.debug(f"Removing group {group_id}")
                self.db.remove_group(group_id)
                self.logger.info(f"Successfully removed group {group_id}")
                
                if self.data_handler:
                    self.data_handler.refresh_data()
                    
        except Exception as e:
            self.logger.error(f"Error removing group: {e}")
            if self.main_window:
                QMessageBox.critical(
                    self.main_window,
                    "エラー",
                    "グループの削除に失敗しました。"
                )

    @pyqtSlot(int)
    def on_group_changed(self, index: int):
        """グループ選択変更処理"""
        self.logger.debug(f"Group selection changed to index {index}")
        
        try:
            if self.data_handler:
                self.data_handler.refresh_user_list()
                
        except Exception as e:
            self.logger.error(f"Error handling group change: {e}")
            if self.main_window:
                QMessageBox.critical(
                    self.main_window,
                    "エラー",
                    "グループ変更の処理に失敗しました。"
                )
