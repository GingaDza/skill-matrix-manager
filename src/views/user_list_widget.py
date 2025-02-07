from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserListWidget(QWidget):
    user_selected = pyqtSignal(int)  # ユーザー選択時のシグナル

    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime.now()
        self.current_user = "GingaDza"
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # ユーザーテーブル
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["ID", "名前", "役割"])
        
        # ヘッダーの設定
        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # ボタン
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("追加")
        self.edit_button = QPushButton("編集")
        self.delete_button = QPushButton("削除")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()

        # レイアウト構築
        layout.addWidget(self.user_table)
        layout.addLayout(button_layout)

        # イベント接続
        self.add_button.clicked.connect(self.add_user)
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.user_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.user_table.itemDoubleClicked.connect(self.on_user_double_clicked)

        # 初期状態
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def load_users(self, group_id=None):
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            if group_id:
                cursor.execute("""
                    SELECT id, name, role 
                    FROM users 
                    WHERE department_id = ?
                    ORDER BY name
                """, (group_id,))
            else:
                cursor.execute("""
                    SELECT id, name, role 
                    FROM users 
                    ORDER BY name
                """)
            
            users = cursor.fetchall()
            self.user_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user[0])))
                self.user_table.setItem(row, 1, QTableWidgetItem(user[1]))
                self.user_table.setItem(row, 2, QTableWidgetItem(user[2] or ""))
                
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            QMessageBox.critical(self, "エラー", f"ユーザーの読み込みに失敗しました: {e}")

    def filter_by_group(self, group_id):
        self.load_users(group_id)

    def on_selection_changed(self):
        has_selection = len(self.user_table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def on_user_double_clicked(self, item):
        row = item.row()
        user_id = int(self.user_table.item(row, 0).text())
        self.user_selected.emit(user_id)

    def add_user(self):
        # TODO: ユーザー追加ダイアログの実装
        pass

    def edit_user(self):
        # TODO: ユーザー編集ダイアログの実装
        pass

    def delete_user(self):
        selected_rows = self.user_table.selectedItems()
        if not selected_rows:
            return
            
        reply = QMessageBox.question(
            self,
            '確認',
            'このユーザーを削除してもよろしいですか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                row = selected_rows[0].row()
                user_id = int(self.user_table.item(row, 0).text())
                
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                
                self.load_users()
                
            except Exception as e:
                logger.error(f"Error deleting user: {e}")
                QMessageBox.critical(self, "エラー", f"ユーザーの削除に失敗しました: {e}")
