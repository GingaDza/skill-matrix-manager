"""カテゴリー管理クラスの実装"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget,
    QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt
from ..dialogs import CategoryDialog
from ...database.database_manager import DatabaseManager
import logging

class CategoryManager(QWidget):
    """カテゴリー管理クラス"""
    
    # カテゴリー選択/変更シグナル
    category_selected = pyqtSignal(str)
    category_added = pyqtSignal()
    category_deleted = pyqtSignal()
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self._db = db_manager
        self.logger = logging.getLogger(__name__)
        self._current_group = ""
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タイトル
        title = QLabel("カテゴリー管理")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # カテゴリー一覧
        self.category_list = QListWidget()
        self.category_list.currentTextChanged.connect(self._on_category_selected)
        layout.addWidget(self.category_list)
        
        # 操作ボタン
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_category)
        button_layout.addWidget(add_button)
        
        edit_button = QPushButton("編集")
        edit_button.clicked.connect(self._edit_category)
        button_layout.addWidget(edit_button)
        
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_category)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_categories(self, group_name: str):
        """カテゴリー一覧を読み込む"""
        self._current_group = group_name
        self.category_list.clear()
        
        if not group_name:
            return
            
        try:
            categories = self._db.get_categories(group_name)
            self.category_list.addItems([cat['name'] for cat in categories])
            
        except Exception as e:
            self.logger.exception("カテゴリーの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"カテゴリーの読み込みに失敗しました: {str(e)}"
            )
    
    def _on_category_selected(self, category_name: str):
        """カテゴリー選択時の処理"""
        self.category_selected.emit(category_name)
    
    def _add_category(self):
        """カテゴリーを追加"""
        if not self._current_group:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return
            
        # 既存のカテゴリー一覧を取得（親カテゴリーの選択用）
        categories = []
        for i in range(self.category_list.count()):
            categories.append(self.category_list.item(i).text())
            
        dialog = CategoryDialog(self, categories=categories)
        if dialog.exec_():
            try:
                self._db.add_category(
                    name=dialog.name,
                    group_name=self._current_group,
                    parent_name=dialog.parent_category
                )
                self.load_categories(self._current_group)
                self.category_added.emit()
                self.logger.info(
                    f"カテゴリーを追加しました: {dialog.name} "
                    f"(グループ: {self._current_group}, "
                    f"親カテゴリー: {dialog.parent_category or 'なし'})"
                )
            except Exception as e:
                self.logger.exception("カテゴリーの追加に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの追加に失敗しました: {str(e)}"
                )
    
    def _edit_category(self):
        """カテゴリーを編集"""
        if not self._current_group:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return
            
        current_item = self.category_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するカテゴリーを選択してください")
            return
            
        old_name = current_item.text()
        
        # 編集対象を除いた既存のカテゴリー一覧を取得（親カテゴリーの選択用）
        categories = []
        for i in range(self.category_list.count()):
            item_text = self.category_list.item(i).text()
            if item_text != old_name:  # 自分自身は除外
                categories.append(item_text)
        
        try:
            current_category = self._db.get_category(
                old_name,
                self._current_group
            )
            parent_name = current_category.get('parent_name', '')
        except Exception as e:
            self.logger.exception("カテゴリー情報の取得に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"カテゴリー情報の取得に失敗しました: {str(e)}"
            )
            return
            
        dialog = CategoryDialog(
            self,
            current_name=old_name,
            categories=categories
        )
        dialog.parent_combo.setCurrentText(parent_name or "なし")
        
        if dialog.exec_():
            try:
                self._db.update_category(
                    old_name=old_name,
                    new_name=dialog.name,
                    group_name=self._current_group,
                    parent_name=dialog.parent_category
                )
                self.load_categories(self._current_group)
                self.category_added.emit()  # 更新も追加として扱う
                self.logger.info(
                    f"カテゴリーを更新しました: {old_name} -> {dialog.name} "
                    f"(グループ: {self._current_group}, "
                    f"親カテゴリー: {dialog.parent_category or 'なし'})"
                )
            except Exception as e:
                self.logger.exception("カテゴリーの更新に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの更新に失敗しました: {str(e)}"
                )
    
    def _delete_category(self):
        """カテゴリーを削除"""
        if not self._current_group:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return
            
        current_item = self.category_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するカテゴリーを選択してください")
            return
            
        name = current_item.text()
        
        reply = QMessageBox.question(
            self,
            "確認",
            f"カテゴリー「{name}」を削除してもよろしいですか？\n"
            "関連するスキルデータもすべて削除されます。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self._db.delete_category(name, self._current_group)
                self.load_categories(self._current_group)
                self.category_deleted.emit()
                self.logger.info(
                    f"カテゴリーを削除しました: {name} "
                    f"(グループ: {self._current_group})"
                )
            except Exception as e:
                self.logger.exception("カテゴリーの削除に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの削除に失敗しました: {str(e)}"
                )
    
    def get_selected_category(self) -> str:
        """選択中のカテゴリー名を取得"""
        current_item = self.category_list.currentItem()
        return current_item.text() if current_item else ""
