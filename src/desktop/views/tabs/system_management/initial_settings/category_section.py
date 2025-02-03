from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QPushButton, QHBoxLayout,
    QListWidget, QLabel, QDialog, QMessageBox,
    QListWidgetItem
)
from ....dialogs.input_dialog import InputDialog
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CategorySection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("カテゴリー管理", parent)
        self.current_time = datetime(2025, 2, 3, 12, 16, 44)
        self.current_user = "GingaDza"
        
        logger.debug(f"{self.current_time} - {self.current_user} CategorySection initialization started")
        self.parent_categories = {}  # グループごとの親カテゴリー
        self.child_categories = {}   # 親カテゴリーごとの子カテゴリー
        self.selected_group = None   # 現在選択されているグループ
        self.setup_ui()
        logger.debug(f"{self.current_time} - {self.current_user} CategorySection initialization completed")

    def setup_ui(self):
        """UIの初期設定"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Setting up CategorySection UI")
            layout = QVBoxLayout()
            
            # 親カテゴリーセクション
            parent_layout = QVBoxLayout()
            parent_label = QLabel("親カテゴリー")
            self.parent_list = QListWidget()
            self.parent_list.itemSelectionChanged.connect(self.on_parent_selection_changed)
            parent_layout.addWidget(parent_label)
            parent_layout.addWidget(self.parent_list)
            
            # 親カテゴリーボタン
            parent_button_layout = QHBoxLayout()
            self.add_parent_btn = QPushButton("追加")
            self.edit_parent_btn = QPushButton("編集")
            self.delete_parent_btn = QPushButton("削除")
            
            for btn in [self.add_parent_btn, self.edit_parent_btn, self.delete_parent_btn]:
                parent_button_layout.addWidget(btn)
            
            parent_layout.addLayout(parent_button_layout)
            
            # 子カテゴリーセクション
            child_layout = QVBoxLayout()
            child_label = QLabel("子カテゴリー（スキル）")
            self.child_list = QListWidget()
            self.child_list.itemSelectionChanged.connect(self.on_child_selection_changed)
            child_layout.addWidget(child_label)
            child_layout.addWidget(self.child_list)
            
            # 子カテゴリーボタン
            child_button_layout = QHBoxLayout()
            self.add_child_btn = QPushButton("追加")
            self.edit_child_btn = QPushButton("編集")
            self.delete_child_btn = QPushButton("削除")
            
            for btn in [self.add_child_btn, self.edit_child_btn, self.delete_child_btn]:
                child_button_layout.addWidget(btn)
            
            child_layout.addLayout(child_button_layout)
            
            # メインレイアウトに追加
            layout.addLayout(parent_layout)
            layout.addLayout(child_layout)
            
            self.setLayout(layout)
            
            # ボタンの接続
            self.setup_connections()
            
            # 初期状態の設定
            self.update_button_states()
            
            logger.debug(f"{self.current_time} - {self.current_user} CategorySection UI setup completed")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in setup_ui: {str(e)}")
            raise

    def setup_connections(self):
        """シグナル/スロット接続の設定"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Setting up button connections")
            
            # 親カテゴリーのボタン接続
            self.add_parent_btn.clicked.connect(self.add_parent_category)
            self.edit_parent_btn.clicked.connect(self.edit_parent_category)
            self.delete_parent_btn.clicked.connect(self.delete_parent_category)
            
            # 子カテゴリーのボタン接続
            self.add_child_btn.clicked.connect(self.add_child_category)
            self.edit_child_btn.clicked.connect(self.edit_child_category)
            self.delete_child_btn.clicked.connect(self.delete_child_category)
            
            logger.debug(f"{self.current_time} - {self.current_user} Button connections completed")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in setup_connections: {str(e)}")
            raise

    def set_selected_group(self, group_name):
        """選択されたグループを設定し、関連するカテゴリーを表示"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Setting selected group to: {group_name}")
            self.selected_group = group_name
            
            # グループが未初期化の場合は初期化
            if group_name not in self.parent_categories:
                self.parent_categories[group_name] = []
                logger.debug(f"{self.current_time} - {self.current_user} Initialized new group: {group_name}")
            
            # 表示を更新
            self.clear_categories()
            self.update_categories_for_group(group_name)
            
            # ボタンの状態を更新
            self.update_button_states()
            
            logger.info(f"{self.current_time} - {self.current_user} Successfully set and displayed group: {group_name}")
            logger.debug(f"{self.current_time} - {self.current_user} Current parent categories: {self.parent_categories}")
            logger.debug(f"{self.current_time} - {self.current_user} Current child categories: {self.child_categories}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error setting selected group: {str(e)}")
            self.show_error(f"グループの設定中にエラーが発生しました: {str(e)}")

    def update_categories_for_group(self, group_name):
        """指定されたグループのカテゴリーを表示"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Updating categories for group: {group_name}")
            
            # 親カテゴリーの表示をクリア
            self.parent_list.clear()
            self.child_list.clear()
            
            # グループに関連する親カテゴリーを表示
            if group_name in self.parent_categories:
                for parent in self.parent_categories[group_name]:
                    item = QListWidgetItem(parent)
                    self.parent_list.addItem(item)
                    logger.debug(f"{self.current_time} - {self.current_user} Added parent category: {parent}")
            
            logger.info(f"{self.current_time} - {self.current_user} Categories updated for group: {group_name}")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error updating categories: {str(e)}")
            self.show_error(f"カテゴリーの更新中にエラーが発生しました: {str(e)}")

    def add_parent_category(self):
        """親カテゴリーを追加"""
        try:
            if self.selected_group is None:
                self.show_error("グループが選択されていません")
                return False

            dialog = InputDialog("親カテゴリー追加", "カテゴリー名:", parent=self)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return False

            name = dialog.get_input().strip()
            if not name:
                return False

            logger.debug(f"{self.current_time} - {self.current_user} Adding parent category: {name} to group: {self.selected_group}")

            # 重複チェック
            if name in self.parent_categories[self.selected_group]:
                self.show_error("同じ名前の親カテゴリーが既に存在します")
                return False

            # 親カテゴリーを追加
            self.parent_categories[self.selected_group].append(name)
            self.child_categories[name] = []

            # リストに表示
            item = QListWidgetItem(name)
            self.parent_list.addItem(item)

            logger.info(f"{self.current_time} - {self.current_user} Successfully added parent category: {name} to group: {self.selected_group}")
            logger.debug(f"{self.current_time} - {self.current_user} Updated parent categories: {self.parent_categories}")
            return True
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error adding parent category: {str(e)}")
            self.show_error(f"親カテゴリーの追加中にエラーが発生しました: {str(e)}")
            return False

    def clear_categories(self):
        """カテゴリーリストをクリア"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Clearing category lists")
            self.parent_list.clear()
            self.child_list.clear()
            logger.debug(f"{self.current_time} - {self.current_user} Category lists cleared successfully")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error clearing categories: {str(e)}")

    def get_selected_category(self):
        """選択された親カテゴリーと子カテゴリーを返す"""
        try:
            parent_item = self.parent_list.currentItem()
            child_item = self.child_list.currentItem()
            
            if parent_item and child_item:
                return (parent_item.text(), child_item.text())
            return None
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error getting selected category: {str(e)}")
            return None

    def update_button_states(self):
        """ボタンの有効/無効状態を更新"""
        try:
            has_group = self.selected_group is not None
            has_parent = self.parent_list.currentItem() is not None
            has_child = self.child_list.currentItem() is not None
            
            # 親カテゴリーボタン
            self.add_parent_btn.setEnabled(has_group)
            self.edit_parent_btn.setEnabled(has_parent)
            self.delete_parent_btn.setEnabled(has_parent)
            
            # 子カテゴリーボタン
            self.add_child_btn.setEnabled(has_parent)
            self.edit_child_btn.setEnabled(has_child)
            self.delete_child_btn.setEnabled(has_child)
            
            logger.debug(f"{self.current_time} - {self.current_user} Button states updated")
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error updating button states: {str(e)}")

    def show_error(self, message):
        """エラーメッセージを表示"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Showing error: {message}")
            QMessageBox.critical(self, "エラー", message)
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error showing error message: {str(e)}")

    def show_confirmation(self, message):
        """確認ダイアログを表示"""
        try:
            logger.debug(f"{self.current_time} - {self.current_user} Showing confirmation: {message}")
            return QMessageBox.question(
                self, "確認", message,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ) == QMessageBox.StandardButton.Yes
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error showing confirmation dialog: {str(e)}")
            return False