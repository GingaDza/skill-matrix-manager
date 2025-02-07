from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QCoreApplication
import logging
import traceback
import sys
from ..database.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)
    data_changed = pyqtSignal()

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Starting MainWindow initialization")
        
        # QApplicationが作成されていることを確認
        if not QCoreApplication.instance():
            self.logger.critical("QApplication not created before MainWindow")
            raise RuntimeError("QApplication must be created before MainWindow")
            
        super().__init__()
        self.logger.debug("MainWindow parent initialization complete")
        
        # クラッシュ時のスタックトレース出力を設定
        sys.excepthook = self._exception_hook
        
        # インスタンス変数の初期化
        self.logger.debug("Initializing instance variables")
        self.db = None
        self.current_user_id = None
        self.current_group_id = None
        self.is_updating = False
        self.buttons = {}  # ボタンの参照を保持
        
        try:
            # データベース接続
            self.logger.debug("Creating database connection")
            self.db = DatabaseManager()
            
            # 更新用タイマー
            self.logger.debug("Setting up refresh timer")
            self.refresh_timer = QTimer()
            self.refresh_timer.setSingleShot(True)
            self.refresh_timer.timeout.connect(self._refresh_data)
            
            # GUI初期化
            self.logger.debug("Initializing GUI")
            self._init_ui()
            self._connect_signals()
            
            self.logger.debug("MainWindow initialization completed successfully")
            
            # 初期データ読み込みをキューに入れる
            QTimer.singleShot(100, self._safe_load_initial_data)
            
        except Exception as e:
            self.logger.critical(f"Failed to initialize MainWindow: {e}\n{traceback.format_exc()}")
            raise

    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        """未捕捉の例外をログに記録"""
        self.logger.critical("Uncaught exception:", 
                           exc_info=(exc_type, exc_value, exc_traceback))

    def _init_ui(self):
        """UIの初期化"""
        self.logger.debug("Starting UI initialization")
        try:
            # ウィンドウ設定
            self.setWindowTitle("スキルマトリックス管理システム")
            self.setMinimumSize(800, 600)
            
            # メインウィジェット
            self.logger.debug("Creating main widget")
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # メインレイアウト
            main_layout = QHBoxLayout(central_widget)
            
            # 左ペイン
            self.logger.debug("Creating left pane")
            left_pane = self._create_left_pane()
            main_layout.addWidget(left_pane, stretch=1)
            
            # 右ペイン
            self.logger.debug("Creating right pane")
            right_pane = QTabWidget()
            main_layout.addWidget(right_pane, stretch=2)
            
            self.logger.debug("UI initialization completed")
            
        except Exception as e:
            self.logger.critical(f"Failed to initialize UI: {e}\n{traceback.format_exc()}")
            raise

    def _create_left_pane(self):
        """左ペインの作成"""
        self.logger.debug("Creating left pane widgets")
        try:
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            
            # グループ選択
            self.logger.debug("Setting up group selection")
            group_label = QLabel("グループ選択:")
            self.group_combo = QComboBox()
            
            # ユーザーリスト
            self.logger.debug("Setting up user list")
            user_label = QLabel("ユーザー一覧:")
            self.user_list = QListWidget()
            
            # ボタン
            self.logger.debug("Creating buttons")
            self.buttons["add"] = QPushButton("ユーザー追加")
            self.buttons["edit"] = QPushButton("ユーザー編集")
            self.buttons["delete"] = QPushButton("ユーザー削除")
            
            # レイアウトに追加
            layout.addWidget(group_label)
            layout.addWidget(self.group_combo)
            layout.addWidget(user_label)
            layout.addWidget(self.user_list)
            layout.addWidget(self.buttons["add"])
            layout.addWidget(self.buttons["edit"])
            layout.addWidget(self.buttons["delete"])
            layout.addStretch()
            
            self.logger.debug("Left pane creation completed")
            return widget
            
        except Exception as e:
            self.logger.critical(f"Failed to create left pane: {e}\n{traceback.format_exc()}")
            raise

    def _connect_signals(self):
        """シグナルの接続"""
        self.logger.debug("Connecting signals")
        try:
            # グループ変更
            self.group_combo.currentIndexChanged.connect(self._on_group_changed)
            
            # データ変更
            self.data_changed.connect(lambda: self.refresh_timer.start(100))
            
            # ボタン接続
            self.buttons["add"].clicked.connect(self._add_user)
            self.buttons["edit"].clicked.connect(self._edit_user)
            self.buttons["delete"].clicked.connect(self._delete_user)
            
            self.logger.debug("Signal connections completed")
            
        except Exception as e:
            self.logger.error(f"Failed to connect signals: {e}\n{traceback.format_exc()}")

    def _edit_user(self):
        """ユーザー編集"""
        self.logger.debug("Starting user edit")
        try:
            current_item = self.user_list.currentItem()
            if not current_item:
                self.logger.warning("No user selected for editing")
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
                self.logger.debug(f"Editing user {user_id} name to '{new_name}'")
                if self.db.edit_user(user_id, new_name.strip()):
                    self.logger.info(f"Successfully edited user {user_id}")
                    self.data_changed.emit()
                    QMessageBox.information(self, "成功", f"ユーザー名を '{new_name}' に変更しました")
                else:
                    self.logger.error(f"Failed to edit user {user_id}")
                    QMessageBox.warning(self, "警告", "ユーザーの編集に失敗しました")
                    
        except Exception as e:
            self.logger.error(f"Error editing user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "ユーザーの編集中にエラーが発生しました")

    def _delete_user(self):
        """ユーザー削除"""
        self.logger.debug("Starting user deletion")
        try:
            current_item = self.user_list.currentItem()
            if not current_item:
                self.logger.warning("No user selected for deletion")
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
                self.logger.debug(f"Deleting user {user_id}")
                if self.db.delete_user(user_id):
                    self.logger.info(f"Successfully deleted user {user_id}")
                    self.user_deleted.emit(user_id)
                    self.data_changed.emit()
                    QMessageBox.information(self, "成功", f"ユーザー '{user_name}' を削除しました")
                else:
                    self.logger.error(f"Failed to delete user {user_id}")
                    QMessageBox.warning(self, "警告", "ユーザーの削除に失敗しました")
                    
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "ユーザーの削除中にエラーが発生しました")

    def _safe_load_initial_data(self):
        """安全な初期データ読み込み"""
        self.logger.debug("Starting safe initial data load")
        try:
            if not self.db:
                self.logger.error("Database connection not available")
                return
                
            if self.is_updating:
                self.logger.debug("Update already in progress, skipping")
                return
                
            self.is_updating = True
            self.logger.debug("Loading initial data")
            
            # グループデータの読み込み
            self.logger.debug("Fetching groups")
            groups = self.db.get_all_groups()
            
            self.logger.debug(f"Found {len(groups)} groups")
            self.group_combo.clear()
            
            for group_id, group_name in groups:
                self.logger.debug(f"Adding group: {group_id} - {group_name}")
                self.group_combo.addItem(group_name, group_id)
            
            # 最初のグループを選択
            if self.group_combo.count() > 0:
                self.logger.debug("Setting initial group selection")
                self.group_combo.setCurrentIndex(0)
                self.current_group_id = self.group_combo.itemData(0)
                self.logger.debug(f"Initial group ID set to: {self.current_group_id}")
            
            self.logger.debug("Initial data load completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading initial data: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "初期データの読み込みに失敗しました")
        finally:
            self.is_updating = False

    def _on_group_changed(self, index):
        """グループ変更時の処理"""
        self.logger.debug(f"Group changed to index {index}")
        if not self.is_updating and index >= 0:
            try:
                self.current_group_id = self.group_combo.itemData(index)
                self.logger.debug(f"New group ID: {self.current_group_id}")
                self._refresh_user_list()
            except Exception as e:
                self.logger.error(f"Error handling group change: {e}\n{traceback.format_exc()}")

    def _add_user(self):
        """ユーザー追加"""
        self.logger.debug("Starting user addition")
        try:
            if self.current_group_id is None:
                self.logger.warning("No group selected for user addition")
                QMessageBox.warning(self, "警告", "グループを選択してください")
                return
                
            name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力してください:")
            if ok and name.strip():
                self.logger.debug(f"Adding user '{name}' to group {self.current_group_id}")
                if self.db.add_user(name.strip(), self.current_group_id):
                    self.logger.info(f"Successfully added user '{name}'")
                    self.data_changed.emit()
                    QMessageBox.information(self, "成功", f"ユーザー '{name}' を追加しました")
                else:
                    self.logger.error("Failed to add user")
                    QMessageBox.warning(self, "警告", "ユーザーの追加に失敗しました")
                    
        except Exception as e:
            self.logger.error(f"Error adding user: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "ユーザーの追加中にエラーが発生しました")

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        self.logger.debug("Processing window close event")
        try:
            self.window_closed.emit()
            self.logger.debug("Window closed signal emitted")
        except Exception as e:
            self.logger.error(f"Error in close event: {e}\n{traceback.format_exc()}")
        finally:
            event.accept()
            self.logger.debug("Window close event accepted")

