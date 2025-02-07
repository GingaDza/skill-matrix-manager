from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from ..database.database_manager import DatabaseManager
import logging

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    window_closed = pyqtSignal()
    user_deleted = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("MainWindow initialization started")
        
        # 基本設定
        self.setWindowTitle("スキルマトリックス管理システム")
        self.setMinimumSize(800, 600)
        
        # インスタンス変数の初期化
        self.db = DatabaseManager()
        self.current_user_id = None
        self.current_group_id = None
        
        # UIの設定
        self._create_ui()
        self._load_initial_data()

    def _create_ui(self):
        """UIの作成"""
        # メインウィジェットとレイアウト
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # 左ペイン（グループとユーザー）
        left_pane = self._create_left_pane()
        layout.addWidget(left_pane)
        
        # 右ペイン（タブ）
        right_pane = QTabWidget()
        layout.addWidget(right_pane)
        
        # レイアウトの調整
        layout.setStretch(0, 1)  # 左ペイン
        layout.setStretch(1, 2)  # 右ペイン

    def _create_left_pane(self):
        """左ペインの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # グループ選択
        group_label = QLabel("グループ選択:")
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self._on_group_changed)
        
        # ユーザーリスト
        user_label = QLabel("ユーザー一覧:")
        self.user_list = QListWidget()
        
        # ボタン
        add_button = QPushButton("ユーザー追加")
        edit_button = QPushButton("ユーザー編集")
        delete_button = QPushButton("ユーザー削除")
        
        # ボタンの接続
        add_button.clicked.connect(self._add_user)
        edit_button.clicked.connect(self._edit_user)
        delete_button.clicked.connect(self._delete_user)
        
        # レイアウトに追加
        layout.addWidget(group_label)
        layout.addWidget(self.group_combo)
        layout.addWidget(user_label)
        layout.addWidget(self.user_list)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        
        return widget

    def _load_initial_data(self):
        """初期データの読み込み"""
        try:
            # グループの読み込み
            groups = self.db.get_all_groups()
            self.group_combo.clear()
            
            for group_id, group_name in groups:
                self.group_combo.addItem(group_name, group_id)
            
            # 最初のグループを選択
            if self.group_combo.count() > 0:
                self.group_combo.setCurrentIndex(0)
        except Exception as e:
            self.logger.error(f"Failed to load initial data: {e}")
            QMessageBox.critical(self, "エラー", "初期データの読み込みに失敗しました")

    def _on_group_changed(self, index):
        """グループ変更時の処理"""
        if index >= 0:
            try:
                group_id = self.group_combo.itemData(index)
                self.current_group_id = group_id
                self._refresh_user_list()
            except Exception as e:
                self.logger.error(f"Error changing group: {e}")
                QMessageBox.critical(self, "エラー", "グループの変更に失敗しました")

    def _refresh_user_list(self):
        """ユーザーリストの更新"""
        try:
            if self.current_group_id is None:
                return
            
            users = self.db.get_users_by_group(self.current_group_id)
            self.user_list.clear()
            
            for user_id, user_name in users:
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                self.user_list.addItem(item)
        except Exception as e:
            self.logger.error(f"Error refreshing user list: {e}")
            QMessageBox.critical(self, "エラー", "ユーザーリストの更新に失敗しました")

    def _add_user(self):
        """ユーザー追加"""
        try:
            if self.current_group_id is None:
                QMessageBox.warning(self, "警告", "グループを選択してください")
                return
            
            name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力してください:")
            if ok and name.strip():
                user_id = self.db.add_user(name.strip(), self.current_group_id)
                if user_id:
                    self._refresh_user_list()
                    QMessageBox.information(self, "成功", f"ユーザー '{name}' を追加しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの追加に失敗しました")
        except Exception as e:
            self.logger.error(f"Error adding user: {e}")
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
                    self._refresh_user_list()
                    QMessageBox.information(self, "成功", f"ユーザー名を '{new_name}' に変更しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの編集に失敗しました")
        except Exception as e:
            self.logger.error(f"Error editing user: {e}")
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
                    self._refresh_user_list()
                    QMessageBox.information(self, "成功", f"ユーザー '{user_name}' を削除しました")
                else:
                    QMessageBox.warning(self, "警告", "ユーザーの削除に失敗しました")
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}")
            QMessageBox.critical(self, "エラー", "ユーザーの削除中にエラーが発生しました")

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        try:
            self.window_closed.emit()
        except Exception as e:
            self.logger.error(f"Error in close event: {e}")
        event.accept()
