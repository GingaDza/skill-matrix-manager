from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class UserDialog(QDialog):
    def __init__(self, group_controller, user=None, parent=None):
        """
        ユーザー追加/編集ダイアログ
        
        Args:
            group_controller: グループコントローラー
            user: 編集対象のユーザー（新規作成時はNone）
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.group_controller = group_controller
        self.user = user
        self.user_data = None
        self.current_time = TimeProvider.get_current_time()
        
        self.setup_ui()
        self.load_groups()
        
        if user:
            self.setWindowTitle("ユーザーの編集")
            self.load_user_data()
        else:
            self.setWindowTitle("ユーザーの追加")
            
    def setup_ui(self):
        """UIのセットアップ"""
        try:
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            
            # 社員番号
            employee_id_layout = QHBoxLayout()
            employee_id_label = QLabel("社員番号:")
            self.employee_id_edit = QLineEdit()
            self.employee_id_edit.setPlaceholderText("例: E001")
            employee_id_layout.addWidget(employee_id_label)
            employee_id_layout.addWidget(self.employee_id_edit)
            layout.addLayout(employee_id_layout)
            
            # 名前
            name_layout = QHBoxLayout()
            name_label = QLabel("名前:")
            self.name_edit = QLineEdit()
            self.name_edit.setPlaceholderText("例: 山田 太郎")
            name_layout.addWidget(name_label)
            name_layout.addWidget(self.name_edit)
            layout.addLayout(name_layout)
            
            # グループ
            group_layout = QHBoxLayout()
            group_label = QLabel("グループ:")
            self.group_combo = QComboBox()
            group_layout.addWidget(group_label)
            group_layout.addWidget(self.group_combo)
            layout.addLayout(group_layout)
            
            # ボタン
            button_layout = QHBoxLayout()
            self.ok_button = QPushButton("OK")
            self.cancel_button = QPushButton("キャンセル")
            button_layout.addWidget(self.ok_button)
            button_layout.addWidget(self.cancel_button)
            layout.addLayout(button_layout)
            
            # シグナル/スロット接続
            self.ok_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            
            # ダイアログのサイズ設定
            self.setMinimumWidth(300)
            
            logger.debug(f"{self.current_time} - UserDialog UI setup completed")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup UserDialog UI: {str(e)}")
            raise
            
    def load_groups(self):
        """グループコンボボックスにグループを読み込む"""
        try:
            groups = self.group_controller.get_all_groups()
            self.group_combo.clear()
            
            # グループなしのオプション
            self.group_combo.addItem("選択なし", None)
            
            # グループの追加
            for group in groups:
                self.group_combo.addItem(group.name, group.id)
                
            logger.debug(f"{self.current_time} - Loaded {len(groups)} groups")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load groups: {str(e)}")
            raise
            
    def load_user_data(self):
        """編集時のユーザーデータを読み込む"""
        try:
            if self.user:
                self.employee_id_edit.setText(self.user.employee_id)
                self.name_edit.setText(self.user.name)
                
                # グループの選択
                if self.user.group_id:
                    index = self.group_combo.findData(self.user.group_id)
                    if index >= 0:
                        self.group_combo.setCurrentIndex(index)
                        
            logger.debug(f"{self.current_time} - Loaded user data for editing")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load user data: {str(e)}")
            raise
            
    def accept(self):
        """OKボタンが押された時の処理"""
        try:
            # 入力値の取得
            employee_id = self.employee_id_edit.text().strip()
            name = self.name_edit.text().strip()
            group_id = self.group_combo.currentData()
            
            # 入力値の検証
            if not employee_id:
                QMessageBox.warning(self, "警告", "社員番号を入力してください。")
                return
                
            if not name:
                QMessageBox.warning(self, "警告", "名前を入力してください。")
                return
                
            # ユーザーデータの設定
            self.user_data = {
                'employee_id': employee_id,
                'name': name,
                'group_id': group_id
            }
            
            logger.debug(f"{self.current_time} - User data validated and accepted")
            super().accept()
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to process user data: {str(e)}")
            QMessageBox.critical(self, "エラー", "データの処理に失敗しました。")
            
    def get_user_data(self):
        """ユーザーデータを取得"""
        return self.user_data