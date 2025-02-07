# src/views/components/user_management.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
import logging

logger = logging.getLogger(__name__)

class UserManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # ユーザー追加フォーム
        form_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("ユーザー名")
        form_layout.addWidget(self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("メールアドレス（任意）")
        form_layout.addWidget(self.email_input)
        
        self.group_combo = QComboBox()
        self.group_combo.setMinimumWidth(150)
        form_layout.addWidget(self.group_combo)
        
        add_btn = QPushButton("追加")
        add_btn.clicked.connect(self.add_user)
        form_layout.addWidget(add_btn)
        
        layout.addLayout(form_layout)

        # ユーザーリスト
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "名前", "メールアドレス", "グループ", "操作"])
        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.user_table)

    def load_data(self):
        try:
            # グループの読み込み
            groups = self.parent.db.get_all_groups()
            self.group_combo.clear()
            for group_id, name, _ in groups:
                self.group_combo.addItem(name, group_id)

            # ユーザーの読み込み
            users = self.parent.db.get_users()
            self.user_table.setRowCount(len(users))
            for row, (user_id, name, email, group_id, group_name) in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
                self.user_table.setItem(row, 1, QTableWidgetItem(name))
                self.user_table.setItem(row, 2, QTableWidgetItem(email or ""))
                self.user_table.setItem(row, 3, QTableWidgetItem(group_name))
                
                delete_btn = QPushButton("削除")
                delete_btn.clicked.connect(lambda checked, uid=user_id: self.delete_user(uid))
                self.user_table.setCellWidget(row, 4, delete_btn)

            logger.debug("User management data loaded successfully")
        except Exception as e:
            logger.error(f"Error loading user management data: {str(e)}")
            QMessageBox.critical(self, "エラー", "データの読み込みに失敗しました。")

    def add_user(self):
        try:
            name = self.name_input.text().strip()
            email = self.email_input.text().strip() or None
            group_id = self.group_combo.currentData()

            if not name:
                QMessageBox.warning(self, "警告", "ユーザー名を入力してください。")
                return

            if not group_id:
                QMessageBox.warning(self, "警告", "グループを選択してください。")
                return

            user_id = self.parent.db.add_user(name, group_id, email)
            self.load_data()  # テーブルを更新
            
            # 入力フィールドをクリア
            self.name_input.clear()
            self.email_input.clear()
            
            logger.debug(f"Added user: {name} (ID: {user_id})")
        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
        except Exception as e:
            logger.error(f"Error adding user: {str(e)}")
            QMessageBox.critical(self, "エラー", "ユーザーの追加に失敗しました。")

    def delete_user(self, user_id):
        try:
            # ユーザー名を取得
            for row in range(self.user_table.rowCount()):
                if self.user_table.item(row, 0).text() == str(user_id):
                    user_name = self.user_table.item(row, 1).text()
                    break
            else:
                raise ValueError("User not found")

            reply = QMessageBox.question(
                self, '確認', 
                f'ユーザー "{user_name}" を削除してもよろしいですか？\n'
                f'※このユーザーのスキルデータも削除されます',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.parent.db.delete_user(user_id)
                self.load_data()  # テーブルを更新
                logger.debug(f"Deleted user: {user_name} (ID: {user_id})")
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            QMessageBox.critical(self, "エラー", "ユーザーの削除に失敗しました。")

    def update_groups(self):
        """グループリストが更新されたときに呼ばれる"""
        try:
            current_group_id = self.group_combo.currentData()
            self.load_data()
            
            # 可能であれば以前選択されていたグループを選択
            if current_group_id is not None:
                index = self.group_combo.findData(current_group_id)
                if index >= 0:
                    self.group_combo.setCurrentIndex(index)
            
            logger.debug("Updated group combo box")
        except Exception as e:
            logger.error(f"Error updating groups: {str(e)}")
