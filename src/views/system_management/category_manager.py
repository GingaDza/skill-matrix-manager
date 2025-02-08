"""カテゴリー管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel,
    QListWidget, QMessageBox, QInputDialog,
    QComboBox, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import Qt
from ...database.database_manager import DatabaseManager
import logging

class CategoryManager(QWidget):
    """カテゴリー管理クラス"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        """初期化"""
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db = db_manager
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentTextChanged.connect(self._on_group_changed)
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)
        
        # カテゴリー追加部分
        add_layout = QHBoxLayout()
        
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("新しいカテゴリー名")
        add_layout.addWidget(self.category_input)
        
        self.parent_combo = QComboBox()
        self.parent_combo.setPlaceholderText("親カテゴリー（オプション）")
        self.parent_combo.addItem("（なし）")
        add_layout.addWidget(self.parent_combo)
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_category)
        add_layout.addWidget(add_button)
        
        layout.addLayout(add_layout)
        
        # カテゴリーツリー
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabels(["カテゴリー", "説明"])
        layout.addWidget(self.category_tree)
        
        # 操作ボタン
        button_layout = QHBoxLayout()
        
        edit_button = QPushButton("編集")
        edit_button.clicked.connect(self._edit_category)
        button_layout.addWidget(edit_button)
        
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_category)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self._load_groups()
    
    def _load_groups(self):
        """グループ一覧を読み込む"""
        self.group_combo.clear()
        try:
            groups = self._db.get_groups()
            self.group_combo.addItems(groups)
        except Exception as e:
            self.logger.exception("グループの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"グループの読み込みに失敗しました: {str(e)}"
            )
    
    def _on_group_changed(self, group_name: str):
        """グループが変更された時の処理"""
        self._load_categories(group_name)
        self._update_parent_combo(group_name)
    
    def _load_categories(self, group_name: str):
        """カテゴリー一覧を読み込む"""
        self.category_tree.clear()
        if not group_name:
            return
            
        try:
            categories = self._db.get_categories(group_name)
            category_map = {}
            root_items = []
            
            # まず親カテゴリーのないアイテムを作成
            for category in categories:
                if not category['parent_name']:
                    item = QTreeWidgetItem([
                        category['name'],
                        category['description'] or ""
                    ])
                    category_map[category['name']] = item
                    root_items.append(item)
            
            # 次に親カテゴリーを持つアイテムを作成
            for category in categories:
                if category['parent_name']:
                    parent_item = category_map.get(category['parent_name'])
                    if parent_item:
                        item = QTreeWidgetItem([
                            category['name'],
                            category['description'] or ""
                        ])
                        parent_item.addChild(item)
                        category_map[category['name']] = item
            
            # ルートアイテムをツリーに追加
            self.category_tree.addTopLevelItems(root_items)
            self.category_tree.expandAll()
            
        except Exception as e:
            self.logger.exception("カテゴリーの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"カテゴリーの読み込みに失敗しました: {str(e)}"
            )
    
    def _update_parent_combo(self, group_name: str):
        """親カテゴリー選択コンボボックスを更新"""
        self.parent_combo.clear()
        self.parent_combo.addItem("（なし）")
        
        if not group_name:
            return
            
        try:
            categories = self._db.get_categories(group_name)
            for category in categories:
                if not category['parent_name']:  # 親カテゴリーのみを追加
                    self.parent_combo.addItem(category['name'])
        except Exception as e:
            self.logger.exception("親カテゴリーの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"親カテゴリーの読み込みに失敗しました: {str(e)}"
            )
    
    def _add_category(self):
        """カテゴリーを追加"""
        group_name = self.group_combo.currentText()
        if not group_name:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return
            
        name = self.category_input.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "カテゴリー名を入力してください")
            return
        
        parent_name = self.parent_combo.currentText()
        if parent_name == "（なし）":
            parent_name = None
        
        description, ok = QInputDialog.getText(
            self,
            "説明の入力",
            "カテゴリーの説明を入力してください:"
        )
        if not ok:
            return
        
        try:
            self._db.add_category(
                name=name,
                group_name=group_name,
                parent_name=parent_name,
                description=description
            )
            self.category_input.clear()
            self._load_categories(group_name)
            self._update_parent_combo(group_name)
            self.logger.info(
                f"カテゴリーを追加しました: {name} "
                f"(グループ: {group_name}, 親カテゴリー: {parent_name or 'なし'})"
            )
        except Exception as e:
            self.logger.exception("カテゴリーの追加に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"カテゴリーの追加に失敗しました: {str(e)}"
            )
    
    def _edit_category(self):
        """選択されたカテゴリーを編集"""
        current = self.category_tree.currentItem()
        if not current:
            QMessageBox.warning(self, "警告", "編集するカテゴリーを選択してください")
            return
        
        group_name = self.group_combo.currentText()
        old_name = current.text(0)
        
        new_name, ok = QInputDialog.getText(
            self,
            "カテゴリー編集",
            "新しいカテゴリー名を入力してください:",
            QLineEdit.Normal,
            old_name
        )
        if not ok or not new_name.strip() or new_name == old_name:
            return
            
        try:
            self._db.update_category(
                old_name=old_name,
                new_name=new_name.strip(),
                group_name=group_name
            )
            self._load_categories(group_name)
            self._update_parent_combo(group_name)
            self.logger.info(
                f"カテゴリーを更新しました: {old_name} -> {new_name} "
                f"(グループ: {group_name})"
            )
        except Exception as e:
            self.logger.exception("カテゴリーの更新に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"カテゴリーの更新に失敗しました: {str(e)}"
            )
    
    def _delete_category(self):
        """選択されたカテゴリーを削除"""
        current = self.category_tree.currentItem()
        if not current:
            QMessageBox.warning(self, "警告", "削除するカテゴリーを選択してください")
            return
            
        group_name = self.group_combo.currentText()
        name = current.text(0)
        
        reply = QMessageBox.question(
            self,
            "確認",
            f"カテゴリー「{name}」を削除してもよろしいですか？\n"
            "サブカテゴリーと関連するスキルもすべて削除されます。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self._db.delete_category(name=name, group_name=group_name)
                self._load_categories(group_name)
                self._update_parent_combo(group_name)
                self.logger.info(
                    f"カテゴリーを削除しました: {name} (グループ: {group_name})"
                )
            except Exception as e:
                self.logger.exception("カテゴリーの削除に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの削除に失敗しました: {str(e)}"
                )
