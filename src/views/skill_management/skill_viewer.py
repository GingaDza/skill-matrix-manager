"""スキルビューアウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget,
    QTreeWidgetItem, QPushButton, QMessageBox
)
from ...database.database_manager import DatabaseManager

class SkillViewer(QWidget):
    """スキルビューアクラス"""
    
    def __init__(self, db_manager: DatabaseManager = None):
        """初期化"""
        super().__init__()
        self._db = db_manager
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # ツリーウィジェット
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["グループ/カテゴリー/スキル"])
        layout.addWidget(self.tree)
        
        # 更新ボタン
        refresh_button = QPushButton("更新")
        refresh_button.clicked.connect(self._load_skills)
        layout.addWidget(refresh_button)
        
        self.setLayout(layout)
        self._load_skills()
    
    def _load_skills(self):
        """スキルツリーを読み込む"""
        self.tree.clear()
        if not self._db:
            return
            
        try:
            # グループを読み込む
            for group in self._db.get_groups():
                group_item = QTreeWidgetItem([group])
                self.tree.addTopLevelItem(group_item)
                
                # カテゴリーを読み込む
                for category in self._db.get_categories(group):
                    category_item = QTreeWidgetItem([category])
                    group_item.addChild(category_item)
                    
                    # スキルを読み込む
                    for skill in self._db.get_skills(category):
                        skill_item = QTreeWidgetItem([skill])
                        category_item.addChild(skill_item)
                        
            self.tree.expandAll()
        except Exception as e:
            QMessageBox.critical(
                self,
                "エラー",
                f"スキルツリーの読み込みに失敗しました: {str(e)}"
            )
