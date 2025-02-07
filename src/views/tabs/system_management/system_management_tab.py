from PyQt6.QtWidgets import (
    QTabWidget, QPushButton, QVBoxLayout, QWidget, 
    QMessageBox, QListWidget, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from .group_manager import GroupManager
import logging

class SystemManagementTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """UIの初期設定"""
        # メインレイアウト
        layout = QVBoxLayout(self)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 初期設定タブ
        self.group_manager = GroupManager(self)
        self.tab_widget.addTab(self.group_manager, "初期設定")

        # データ入出力タブ
        # self.io_tab = DataIOTab(self)
        # self.tab_widget.addTab(self.io_tab, "データ入出力")

        # システム情報タブ
        # self.info_tab = SystemInfoTab(self)
        # self.tab_widget.addTab(self.info_tab, "システム情報")

        # 新規タブ追加ボタン
        self.add_tab_btn = QPushButton("新規タブ追加")
        self.add_tab_btn.clicked.connect(self.add_new_category_tab)
        layout.addWidget(self.add_tab_btn)

    def load_data(self):
        """データの読み込み"""
        try:
            self.group_manager.load_groups()
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")

    def add_new_category_tab(self):
        """新規カテゴリータブの追加"""
        try:
            # 親カテゴリーが選択されているか確認
            category_list = self.group_manager.category_list
            if not category_list or not category_list.selectedItems():
                QMessageBox.warning(self, "警告", "親カテゴリーを選択してください")
                return

            selected_category = category_list.selectedItems()[0]
            category_name = selected_category.text()
            category_id = selected_category.data(Qt.ItemDataRole.UserRole)

            # 既存のタブをチェック
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == category_name:
                    self.tab_widget.setCurrentIndex(i)
                    return

            # 新しいタブを作成して追加
            new_tab = CategoryContentTab(self, category_id, category_name)
            self.tab_widget.addTab(new_tab, category_name)
            self.tab_widget.setCurrentWidget(new_tab)
            
            self.logger.debug(f"Added new category tab: {category_name}")
            
        except Exception as e:
            self.logger.error(f"Error adding new category tab: {str(e)}")
            QMessageBox.warning(self, "エラー", f"タブの追加に失敗しました: {str(e)}")

class CategoryContentTab(QWidget):
    def __init__(self, parent, category_id, category_name):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.category_id = category_id
        self.category_name = category_name
        self.setup_ui()

    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # カテゴリー情報
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.addWidget(QLabel(f"カテゴリー: {self.category_name}"))
        layout.addWidget(header)
        
        # スキル一覧
        self.skill_list = QListWidget()
        layout.addWidget(self.skill_list)
        
        # ボタン
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_skill_btn = QPushButton("スキル編集")
        self.delete_skill_btn = QPushButton("スキル削除")
        
        self.add_skill_btn.clicked.connect(self.add_skill)
        self.edit_skill_btn.clicked.connect(self.edit_skill)
        self.delete_skill_btn.clicked.connect(self.delete_skill)
        
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_skill_btn)
        button_layout.addWidget(self.delete_skill_btn)
        
        layout.addWidget(button_widget)

    def add_skill(self):
        """スキルの追加"""
        try:
            self.logger.debug(f"Adding skill to category {self.category_name}")
            # スキル追加の実装
            pass
        except Exception as e:
            self.logger.error(f"Error adding skill: {str(e)}")

    def edit_skill(self):
        """スキルの編集"""
        try:
            self.logger.debug(f"Editing skill in category {self.category_name}")
            # スキル編集の実装
            pass
        except Exception as e:
            self.logger.error(f"Error editing skill: {str(e)}")

    def delete_skill(self):
        """スキルの削除"""
        try:
            self.logger.debug(f"Deleting skill from category {self.category_name}")
            # スキル削除の実装
            pass
        except Exception as e:
            self.logger.error(f"Error deleting skill: {str(e)}")
