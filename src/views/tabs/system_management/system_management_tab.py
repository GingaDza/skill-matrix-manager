from PyQt6.QtWidgets import QTabWidget, QPushButton, QVBoxLayout, QWidget, QMessageBox
from .group_manager import GroupManager
import logging

class SystemManagementTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """UIの初期設定"""
        # メインのコンテナウィジェット
        container = QWidget()
        main_layout = QVBoxLayout(container)
        
        # タブウィジェットを作成
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
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
        main_layout.addWidget(self.add_tab_btn)

        # メインレイアウトを設定
        self.setLayout(main_layout)

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
        self.category_id = category_id
        self.category_name = category_name
        self.setup_ui()

    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # カテゴリー情報
        layout.addWidget(QLabel(f"カテゴリー: {self.category_name}"))
        
        # スキル一覧
        self.skill_list = QListWidget()
        layout.addWidget(self.skill_list)
        
        # ボタン
        button_layout = QHBoxLayout()
        
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_skill_btn = QPushButton("スキル編集")
        self.delete_skill_btn = QPushButton("スキル削除")
        
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_skill_btn)
        button_layout.addWidget(self.delete_skill_btn)
        
        layout.addLayout(button_layout)
