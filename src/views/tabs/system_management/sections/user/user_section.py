from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QComboBox, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserSection(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime.now()
        self.current_user = "GingaDza"
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # グループ選択
        group_layout = QHBoxLayout()
        group_label = QLabel("グループ:")
        self.group_combo = QComboBox()
        self.load_groups()
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        group_layout.addStretch()

        # ユーザーテーブル
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "名前", "グループ", "役割"])
        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # ボタン
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("追加")
        self.edit_button = QPushButton("編集")
        self.delete_button = QPushButton("削除")
        self.export_button = QPushButton("エクスポート")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.export_button)

        # レイアウト構築
        layout.addLayout(group_layout)
        layout.addWidget(self.user_table)
        layout.addLayout(button_layout)

        # イベント接続
        self.add_button.clicked.connect(self.add_user)
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.export_button.clicked.connect(self.export_users)
        self.group_combo.currentIndexChanged.connect(self.load_users)
        self.user_table.itemSelectionChanged.connect(self.on_selection_changed)

        # 初期状態
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def load_groups(self):
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name FROM departments ORDER BY name")
            groups = cursor.fetchall()
            
            self.group_combo.clear()
            self.group_combo.addItem("全てのグループ", None)
            for group in groups:
                self.group_combo.addItem(group[1], group[0])
                
        except Exception as e:
            logger.error(f"Error loading groups: {e}")
            QMessageBox.critical(self, "エラー", f"グループの読み込みに失敗しました: {e}")

    def load_users(self):
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            group_id = self.group_combo.currentData()
            
            if group_id:
                cursor.execute("""
                    SELECT u.id, u.name, d.name, u.role 
                    FROM users u 
                    JOIN departments d ON u.department_id = d.id 
                    WHERE u.department_id = ?
                    ORDER BY u.name
                """, (group_id,))
            else:
                cursor.execute("""
                    SELECT u.id, u.name, d.name, u.role 
                    FROM users u 
                    JOIN departments d ON u.department_id = d.id 
                    ORDER BY u.name
                """)
            
            users = cursor.fetchall()
            self.user_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user[0])))
                self.user_table.setItem(row, 1, QTableWidgetItem(user[1]))
                self.user_table.setItem(row, 2, QTableWidgetItem(user[2]))
                self.user_table.setItem(row, 3, QTableWidgetItem(user[3] or ""))
                
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            QMessageBox.critical(self, "エラー", f"ユーザーの読み込みに失敗しました: {e}")

    def on_selection_changed(self):
        has_selection = len(self.user_table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

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

    def export_users(self):
        # TODO: ユーザーリストのエクスポート機能の実装
        pass
