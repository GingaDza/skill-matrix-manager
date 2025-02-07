from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt

class CategoryTreeWidget(QTreeWidget):
    """カテゴリーツリーを表示するウィジェット"""
    
    category_selected = pyqtSignal(int)  # カテゴリー選択時のシグナル

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db if db else parent.db
        self.setup_ui()
        self.load_categories()

    def setup_ui(self):
        """UIの初期設定"""
        self.setHeaderLabels(["カテゴリー", "スキル数"])
        self.setAlternatingRowColors(True)
        self.itemClicked.connect(self._on_item_clicked)

    def load_categories(self):
        """カテゴリー一覧の読み込み"""
        self.clear()
        categories = self.db.get_all_categories_with_skills()
        
        # カテゴリーツリーの構築
        items = {}
        root_items = []
        
        for category in categories:
            item = QTreeWidgetItem([
                str(category[1]),  # name
                str(category[6] or 0)  # skill_count
            ])
            item.setData(0, Qt.ItemDataRole.UserRole, category[0])  # id
            items[category[0]] = item
            
            if category[3] is None:  # parent_id is None
                root_items.append(item)
            else:
                parent_item = items.get(category[3])
                if parent_item:
                    parent_item.addChild(item)
                else:
                    root_items.append(item)
        
        # ルートアイテムの追加
        self.addTopLevelItems(root_items)
        self.expandAll()

    def _on_item_clicked(self, item, column):
        """アイテムクリック時の処理"""
        category_id = item.data(0, Qt.ItemDataRole.UserRole)
        self.category_selected.emit(category_id)

    def refresh(self):
        """表示の更新"""
        self.load_categories()

    def get_selected_category_id(self):
        """選択されているカテゴリーのIDを取得"""
        current = self.currentItem()
        if current:
            return current.data(0, Qt.ItemDataRole.UserRole)
        return None
