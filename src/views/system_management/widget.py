"""システム管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel,
    QListWidget, QTreeWidget, QTreeWidgetItem,
    QComboBox, QSpacerItem, QSizePolicy,
    QScrollArea, QFrame, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from .group_manager import GroupManager
from .category_manager import CategoryManager
from ..data_management import DataManagementWidget
from ..custom_tab import CategoryTab
from ...database.database_manager import DatabaseManager
import platform
import psutil
import logging

class SystemSettingsTab(QWidget):
    """システム設定タブ"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self._db = db_manager
        self.logger = logging.getLogger(__name__)
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # リストとボタンのコンテナ
        lists_layout = QHBoxLayout()
        
        # グループリスト
        group_container = QVBoxLayout()
        group_container.addWidget(QLabel("グループ"))
        
        self.group_list = QListWidget()
        self.group_list.currentItemChanged.connect(self._on_group_changed)
        group_container.addWidget(self.group_list)
        
        group_buttons = QVBoxLayout()
        add_group_btn = QPushButton("追加")
        add_group_btn.clicked.connect(self._add_group)
        group_buttons.addWidget(add_group_btn)
        
        edit_group_btn = QPushButton("編集")
        edit_group_btn.clicked.connect(self._edit_group)
        group_buttons.addWidget(edit_group_btn)
        
        delete_group_btn = QPushButton("削除")
        delete_group_btn.clicked.connect(self._delete_group)
        group_buttons.addWidget(delete_group_btn)
        
        group_container.addLayout(group_buttons)
        lists_layout.addLayout(group_container)
        
        # カテゴリーリスト
        category_container = QVBoxLayout()
        category_container.addWidget(QLabel("カテゴリー"))
        
        self.category_list = QTreeWidget()
        self.category_list.setHeaderLabels(["名前", "説明"])
        self.category_list.currentItemChanged.connect(self._on_category_changed)
        category_container.addWidget(self.category_list)
        
        category_buttons = QVBoxLayout()
        add_category_btn = QPushButton("追加")
        add_category_btn.clicked.connect(self._add_category)
        category_buttons.addWidget(add_category_btn)
        
        edit_category_btn = QPushButton("編集")
        edit_category_btn.clicked.connect(self._edit_category)
        category_buttons.addWidget(edit_category_btn)
        
        delete_category_btn = QPushButton("削除")
        delete_category_btn.clicked.connect(self._delete_category)
        category_buttons.addWidget(delete_category_btn)
        
        category_container.addLayout(category_buttons)
        lists_layout.addLayout(category_container)
        
        # スキルリスト
        skill_container = QVBoxLayout()
        skill_container.addWidget(QLabel("スキル"))
        
        self.skill_list = QListWidget()
        skill_container.addWidget(self.skill_list)
        
        skill_buttons = QVBoxLayout()
        add_skill_btn = QPushButton("追加")
        add_skill_btn.clicked.connect(self._add_skill)
        skill_buttons.addWidget(add_skill_btn)
        
        edit_skill_btn = QPushButton("編集")
        edit_skill_btn.clicked.connect(self._edit_skill)
        skill_buttons.addWidget(edit_skill_btn)
        
        delete_skill_btn = QPushButton("削除")
        delete_skill_btn.clicked.connect(self._delete_skill)
        skill_buttons.addWidget(delete_skill_btn)
        
        skill_container.addLayout(skill_buttons)
        lists_layout.addLayout(skill_container)
        
        layout.addLayout(lists_layout)
        
        # 新規タブ追加ボタン
        add_tab_btn = QPushButton("選択したカテゴリーで新規タブを追加")
        add_tab_btn.clicked.connect(self._add_custom_tab)
        layout.addWidget(add_tab_btn)
        
        self.setLayout(layout)
        self._load_groups()
    
    def _load_groups(self):
        """グループ一覧を読み込む"""
        self.group_list.clear()
        try:
            groups = self._db.get_groups()
            self.group_list.addItems(groups)
        except Exception as e:
            self.logger.exception("グループの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"グループの読み込みに失敗しました: {str(e)}"
            )
    
    def _on_group_changed(self, current, previous):
        """グループ選択変更時の処理"""
        if current:
            self._load_categories(current.text())
    
    def _load_categories(self, group_name: str):
        """カテゴリー一覧を読み込む"""
        self.category_list.clear()
        if not group_name:
            return
            
        try:
            categories = self._db.get_categories(group_name)
            items = {}
            root_items = []
            
            # まず親カテゴリーのないアイテムを作成
            for category in categories:
                if not category['parent_name']:
                    item = QTreeWidgetItem([
                        category['name'],
                        category['description'] or ""
                    ])
                    items[category['name']] = item
                    root_items.append(item)
            
            # 次に親カテゴリーを持つアイテムを作成
            for category in categories:
                if category['parent_name']:
                    parent_item = items.get(category['parent_name'])
                    if parent_item:
                        item = QTreeWidgetItem([
                            category['name'],
                            category['description'] or ""
                        ])
                        parent_item.addChild(item)
                        items[category['name']] = item
            
            self.category_list.addTopLevelItems(root_items)
            self.category_list.expandAll()
            
        except Exception as e:
            self.logger.exception("カテゴリーの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"カテゴリーの読み込みに失敗しました: {str(e)}"
            )
    
    def _on_category_changed(self, current, previous):
        """カテゴリー選択変更時の処理"""
        if current:
            group_item = self.group_list.currentItem()
            if group_item:
                self._load_skills(group_item.text(), current.text(0))
    
    def _load_skills(self, group_name: str, category_name: str):
        """スキル一覧を読み込む"""
        self.skill_list.clear()
        if not group_name or not category_name:
            return
            
        try:
            skills = self._db.get_skills(category_name, group_name)
            self.skill_list.addItems(skills)
        except Exception as e:
            self.logger.exception("スキルの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"スキルの読み込みに失敗しました: {str(e)}"
            )
    
    def _add_custom_tab(self):
        """新規カスタムタブを追加"""
        current_category = self.category_list.currentItem()
        if not current_category:
            QMessageBox.warning(
                self,
                "警告",
                "新規タブを追加するカテゴリーを選択してください"
            )
            return
            
        group_item = self.group_list.currentItem()
        if not group_item:
            QMessageBox.warning(
                self,
                "警告",
                "グループを選択してください"
            )
            return
            
        try:
            # カテゴリータブを作成
            category_tab = CategoryTab(
                self._db,
                group_item.text(),
                current_category.text(0)
            )
            
            # メインウィンドウのタブウィジェットに追加
            main_window = self.window()
            if main_window:
                main_window.add_custom_tab(
                    current_category.text(0),
                    category_tab
                )
                self.logger.info(
                    f"新規タブを追加しました: {current_category.text(0)}"
                )
        except Exception as e:
            self.logger.exception("新規タブの追加に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"新規タブの追加に失敗しました: {str(e)}"
            )

    # 以下、各種操作メソッド...
