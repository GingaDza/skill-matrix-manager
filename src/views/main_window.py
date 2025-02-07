from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from ..database.database_manager import DatabaseManager
import logging
import traceback

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)
    data_changed = pyqtSignal()  # データ変更通知用シグナル

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("MainWindow initialization started")
        
        # インスタンス変数の初期化
        self.db = DatabaseManager()
        self.current_user_id = None
        self.current_group_id = None
        self.is_updating = False
        
        # 更新用タイマー
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self._refresh_data)
        
        # GUI初期化
        self._init_ui()
        self._connect_signals()
        
        # 初期データ読み込み
        self.refresh_timer.start(100)

    def _init_ui(self):
        """UIの初期化"""
        try:
            self.setWindowTitle("スキルマトリックス管理システム")
            self.setMinimumSize(800, 600)
            
            # メインウィジェット
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # メインレイアウト
            main_layout = QHBoxLayout(central_widget)
            
            # 左ペイン
            left_pane = self._create_left_pane()
            main_layout.addWidget(left_pane, stretch=1)
            
            # 右ペイン
            right_pane = QTabWidget()
            main_layout.addWidget(right_pane, stretch=2)
            
        except Exception as e:
            self.logger.error(f"Error initializing UI: {e}\n{traceback.format_exc()}")
            raise

    def _create_left_pane(self):
        """左ペインの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # グループ選択
        group_label = QLabel("グループ選択:")
        self.group_combo = QComboBox()
        
        # ユーザーリスト
        user_label = QLabel("ユーザー一覧:")
        self.user_list = QListWidget()
        
        # ボタン
        add_button = QPushButton("ユーザー追加")
        edit_button = QPushButton("ユーザー編集")
        delete_button = QPushButton("ユーザー削除")
        
        # レイアウトに追加
        layout.addWidget(group_label)
        layout.addWidget(self.group_combo)
        layout.addWidget(user_label)
        layout.addWidget(self.user_list)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.addStretch()
        
        return widget

    def _connect_signals(self):
        """シグナルの接続"""
        try:
            self.group_combo.currentIndexChanged.connect(self._on_group_changed)
            self.data_changed.connect(lambda: self.refresh_timer.start(100))
            self.findChild(QPushButton, "").clicked.connect(self._add_user)
            self.findChild(QPushButton, "").clicked.connect(self._edit_user)
            self.findChild(QPushButton, "").clicked.connect(self._delete_user)
        except Exception as e:
            self.logger.error(f"Error connecting signals: {e}\n{traceback.format_exc()}")

    def _refresh_data(self):
        """データの更新"""
        if self.is_updating:
            return
            
        try:
            self.is_updating = True
            self.logger.debug("Refreshing data")
            
            # グループデータの更新
            groups = self.db.get_all_groups()
            current_index = self.group_combo.currentIndex()
            current_group_id = self.group_combo.itemData(current_index) if current_index >= 0 else None
            
            self.group_combo.clear()
            for group_id, group_name in groups:
                self.group_combo.addItem(group_name, group_id)
                
            # 現在のグループを再選択
            if current_group_id is not None:
                index = self.group_combo.findData(current_group_id)
                if index >= 0:
                    self.group_combo.setCurrentIndex(index)
            elif self.group_combo.count() > 0:
                self.group_combo.setCurrentIndex(0)
                
            # ユーザーリストの更新
            self._refresh_user_list()
            
        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "データの更新に失敗しました")
        finally:
            self.is_updating = False

    def _refresh_user_list(self):
        """ユーザーリストの更新"""
        try:
            group_id = self.group_combo.currentData()
            if group_id is None:
                return
                
            users = self.db.get_users_by_group(group_id)
            self.user_list.clear()
            
            for user_id, user_name in users:
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                self.user_list.addItem(item)
                
        except Exception as e:
            self.logger.error(f"Error refreshing user list: {e}\n{traceback.format_exc()}")

    def _on_group_changed(self, index):
        """グループ変更時の処理"""
        if not self.is_updating and index >= 0:
            self.current_group_id = self.group_combo.itemData(index)
            self.refresh_timer.start(100)

    def _add_user(self):
        """ユーザー追加"""
        try:
            if self.current_group_id is None:
                QMessageBox.warning(self, "警告", "グループを選択してください")
                return
                
            name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力してください:")
            if ok and name.strip():
                if self.db.add_user(name.strip(), self.current_group_id):
                    self.data_changed.emit()
                    QMessageBox.information(self, "成功", f"ユーザー '{name}' を追加しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの追加に失敗しました")
                    
        except Exception as e:
            self.logger.error(f"Error adding user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "ユーザーの追加中にエラーが発生しました")

    def _edit_user(self):
        """ユーザー編集"""
        try:
            current_item = self.user_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "編集するユーザーを選択してください")
                return
                
            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            current_name = current_item.text()
            
            new_name, ok = QInputDialog.getText(
                self, "ユーザー編集",
                "新しいユーザー名を入力してください:",
                text=current_name
            )
            
            if ok and new_name.strip():
                if self.db.edit_user(user_id, new_name.strip()):
                    self.data_changed.emit()
                    QMessageBox.information(self, "成功", f"ユーザー名を '{new_name}' に変更しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの編集に失敗しました")
                    
        except Exception as e:
            self.logger.error(f"Error editing user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "ユーザーの編集中にエラーが発生しました")

    def _delete_user(self):
        """ユーザー削除"""
        try:
            current_item = self.user_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "警告", "削除するユーザーを選択してください")
                return
                
            user_id = current_item.data(Qt.ItemDataRole.UserRole)
            user_name = current_item.text()
            
            reply = QMessageBox.question(
                self, "確認",
                f"ユーザー '{user_name}' を削除してもよろしいですか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self.db.delete_user(user_id):
                    self.user_deleted.emit(user_id)
                    self.data_changed.emit()
                    QMessageBox.information(self, "成功", f"ユーザー '{user_name}' を削除しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの削除に失敗しました")
                    
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "ユーザーの削除中にエラーが発生しました")

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        try:
            self.window_closed.emit()
        except Exception as e:
            self.logger.error(f"Error in close event: {e}\n{traceback.format_exc()}")
        finally:
            event.accept()
