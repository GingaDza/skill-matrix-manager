from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QListWidget, QLabel,
    QSplitter
)
from PyQt6.QtCore import Qt
import logging
from datetime import datetime
from ..category.category_section import CategorySection
from ..group.group_section import GroupSection

logger = logging.getLogger(__name__)

class InitialSettingsTab(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime.now()
        self.current_user = "GingaDza"
        self.setup_ui()

    def setup_ui(self):
        try:
            layout = QVBoxLayout(self)

            # メインスプリッター（グループとカテゴリーの区切り）
            splitter = QSplitter(Qt.Orientation.Horizontal)
            
            # グループセクション
            group_container = QWidget()
            group_layout = QVBoxLayout(group_container)
            group_label = QLabel("グループ管理")
            self.group_section = GroupSection(self.controllers)
            group_layout.addWidget(group_label)
            group_layout.addWidget(self.group_section)
            
            # カテゴリーセクション
            category_container = QWidget()
            category_layout = QVBoxLayout(category_container)
            category_label = QLabel("カテゴリー管理")
            self.category_section = CategorySection(self.controllers)
            category_layout.addWidget(category_label)
            category_layout.addWidget(self.category_section)
            
            # スプリッターに追加
            splitter.addWidget(group_container)
            splitter.addWidget(category_container)
            
            # 新規タブ追加ボタン
            self.add_tab_button = QPushButton("新規タブ追加")
            self.add_tab_button.clicked.connect(self.add_new_tab)
            
            layout.addWidget(splitter)
            layout.addWidget(self.add_tab_button)
            
        except Exception as e:
            logger.error(f"Error in InitialSettingsTab UI setup: {e}")
            logger.exception("Detailed traceback:")
            raise

    def add_new_tab(self):
        try:
            # 選択された親カテゴリーに基づいて新規タブを生成
            selected_category = self.category_section.get_selected_parent_category()
            if selected_category:
                self.parent().parent().add_custom_tab(selected_category)
            else:
                logger.warning("No parent category selected")
                
        except Exception as e:
            logger.error(f"Error adding new tab: {e}")
            logger.exception("Detailed traceback:")
