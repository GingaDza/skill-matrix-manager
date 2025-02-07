from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QComboBox, QLabel, QPushButton,
    QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
import logging
from src.desktop.utils.time_utils import TimeProvider
from src.desktop.views.components.users.user_list_widget import UserListWidget
from src.desktop.views.dialogs.user_dialog import UserDialog

logger = logging.getLogger(__name__)

class MainPanel(QWidget):
    def __init__(self, user_controller, group_controller, parent=None):
        super().__init__(parent)
        self.user_controller = user_controller
        self.group_controller = group_controller
        self.current_time = TimeProvider.get_current_time()
        
        # UIの初期化
        self.init_ui()
        
        # グループの読み込み
        self.load_groups()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            # メインレイアウト
            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)
            
            # グループ選択エリア
            group_layout = QHBoxLayout()
            group_label = QLabel("グループ:")
            self.group_combo = QComboBox()
            self.group_combo.setMinimumHeight(30)
            group_layout.addWidget(group_label)
            group_layout.addWidget(self.group_combo)
            layout.addLayout(group_layout)
            
            # ユーザーリスト
            self.user_list = UserListWidget(self.user_controller)
            layout.addWidget(self.user_list)
            
            # ボタングループ
            button_layout = QVBoxLayout()
            
            # ユーザー管理ボタン
            user_buttons_layout = QHBoxLayout()
            self.add_button = QPushButton("追加")
            self.edit_button = QPushButton("編集")
            self.delete_button = QPushButton("削除")
            user_buttons_layout.addWidget(self.add_button)
            user_buttons_layout.addWidget(self.edit_button)
            user_buttons_layout.addWidget(self.delete_button)
            button_layout.addLayout(user_buttons_layout)
            
            # 出力ボタン
            export_buttons_layout = QHBoxLayout()
            self.export_pdf_button = QPushButton("PDFレーダーチャート出力")
            self.export_excel_button = QPushButton("Excelスキルレベル出力")
            export_buttons_layout.addWidget(self.export_pdf_button)
            export_buttons_layout.addWidget(self.export_excel_button)
            button_layout.addLayout(export_buttons_layout)
            
            layout.addLayout(button_layout)
            
            # シグナル/スロット接続
            self.setup_connections()
            
            logger.debug(f"{self.current_time} - MainPanel UI initialized successfully")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to initialize MainPanel UI: {str(e)}")
            raise
            
    def setup_connections(self):
        """シグナル/スロットの接続"""
        try:
            self.group_combo.currentIndexChanged.connect(self.on_group_changed)
            self.add_button.clicked.connect(self.on_add_clicked)
            self.edit_button.clicked.connect(self.on_edit_clicked)
            self.delete_button.clicked.connect(self.on_delete_clicked)
            self.export_pdf_button.clicked.connect(self.on_export_pdf_clicked)
            self.export_excel_button.clicked.connect(self.on_export_excel_clicked)
            
            logger.debug(f"{self.current_time} - Connections setup completed")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to setup connections: {str(e)}")
            raise
            
    def load_groups(self):
        """グループコンボボックスにグループを読み込む"""
        try:
            # グループコントローラーからグループリストを取得
            groups = self.group_controller.get_all_groups()
            
            # コンボボックスをクリア
            self.group_combo.clear()
            
            # 「全て」のオプションを追加
            self.group_combo.addItem("全て", None)
            
            # グループを追加
            for group in groups:
                self.group_combo.addItem(group.name, group.id)
                
            logger.debug(f"{self.current_time} - Loaded {len(groups)} groups")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load groups: {str(e)}")
            raise
            
    def on_group_changed(self, index):
        """グループ選択変更時のイベントハンドラ"""
        try:
            group_id = self.group_combo.currentData()
            self.update_user_list(group_id)
            logger.debug(f"{self.current_time} - Group selection changed to ID: {group_id}")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to handle group change: {str(e)}")
            QMessageBox.warning(self, "エラー", f"グループの変更に失敗しました: {str(e)}")
            
    def on_add_clicked(self):
        """ユーザー追加ボタンのイベントハンドラ"""
        try:
            dialog = UserDialog(self.group_controller, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted and dialog.user_data:
                user = self.user_controller.create_user(
                    employee_id=dialog.user_data['employee_id'],
                    name=dialog.user_data['name'],
                    group_id=dialog.user_data['group_id']
                )
                self.update_user_list(self.group_combo.currentData())
                logger.debug(f"{self.current_time} - Added new user: {user.name}")
                QMessageBox.information(self, "成功", "ユーザーを追加しました。")
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to add user: {str(e)}")
            QMessageBox.critical(self, "エラー", f"ユーザーの追加に失敗しました: {str(e)}")
            
    def on_edit_clicked(self):
        """ユーザー編集ボタンのイベントハンドラ"""
        try:
            selected_user = self.user_list.get_selected_user()
            if not selected_user:
                QMessageBox.warning(self, "警告", "編集するユーザーを選択してください。")
                return
                
            dialog = UserDialog(self.group_controller, user=selected_user, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted and dialog.user_data:
                user = self.user_controller.update_user(
                    selected_user.id,
                    employee_id=dialog.user_data['employee_id'],
                    name=dialog.user_data['name'],
                    group_id=dialog.user_data['group_id']
                )
                self.update_user_list(self.group_combo.currentData())
                logger.debug(f"{self.current_time} - Updated user: {user.name}")
                QMessageBox.information(self, "成功", "ユーザー情報を更新しました。")
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to edit user: {str(e)}")
            QMessageBox.critical(self, "エラー", f"ユーザーの編集に失敗しました: {str(e)}")
            
    def on_delete_clicked(self):
        """ユーザー削除ボタンのイベントハンドラ"""
        try:
            selected_user = self.user_list.get_selected_user()
            if not selected_user:
                QMessageBox.warning(self, "警告", "削除するユーザーを選択してください。")
                return
                
            reply = QMessageBox.question(
                self,
                "確認",
                f"ユーザー「{selected_user.name}」を削除しますか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.user_controller.delete_user(selected_user.id)
                self.update_user_list(self.group_combo.currentData())
                logger.debug(f"{self.current_time} - Deleted user: {selected_user.name}")
                QMessageBox.information(self, "成功", "ユーザーを削除しました。")
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete user: {str(e)}")
            QMessageBox.critical(self, "エラー", f"ユーザーの削除に失敗しました: {str(e)}")
            
    def on_export_pdf_clicked(self):
        """PDFレーダーチャート出力ボタンのイベントハンドラ"""
        try:
            selected_user = self.user_list.get_selected_user()
            if not selected_user:
                QMessageBox.warning(self, "警告", "出力するユーザーを選択してください。")
                return
                
            logger.debug(f"{self.current_time} - PDF export requested for user: {selected_user.name}")
            QMessageBox.information(self, "情報", "PDF出力機能は現在開発中です。")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to export PDF: {str(e)}")
            QMessageBox.critical(self, "エラー", f"PDF出力に失敗しました: {str(e)}")
            
    def on_export_excel_clicked(self):
        """Excelスキルレベル出力ボタンのイベントハンドラ"""
        try:
            selected_user = self.user_list.get_selected_user()
            if not selected_user:
                QMessageBox.warning(self, "警告", "出力するユーザーを選択してください。")
                return
                
            logger.debug(f"{self.current_time} - Excel export requested for user: {selected_user.name}")
            QMessageBox.information(self, "情報", "Excel出力機能は現在開発中です。")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to export Excel: {str(e)}")
            QMessageBox.critical(self, "エラー", f"Excel出力に失敗しました: {str(e)}")
            
    def update_user_list(self, group_id=None):
        """ユーザーリストの更新"""
        try:
            if group_id is None:
                users = self.user_controller.get_all_users()
            else:
                users = self.user_controller.get_users_by_group(group_id)
                
            self.user_list.clear()
            for user in users:
                self.user_list.add_user(user)
                
            logger.debug(f"{self.current_time} - Updated user list with {len(users)} users")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to update user list: {str(e)}")
            raise