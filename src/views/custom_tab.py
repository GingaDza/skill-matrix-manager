"""カスタムタブの実装"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame
)
from ..database.database_manager import DatabaseManager
import logging

class CategoryTab(QWidget):
    """カテゴリータブ"""
    
    def __init__(self, db_manager: DatabaseManager, group_name: str, category_name: str, parent=None):
        super().__init__(parent)
        self._db = db_manager
        self._group_name = group_name
        self._category_name = category_name
        self.logger = logging.getLogger(__name__)
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # ヘッダー
        header = QFrame()
        header.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout()
        
        header_layout.addWidget(QLabel(f"グループ: {self._group_name}"))
        header_layout.addWidget(QLabel(f"カテゴリー: {self._category_name}"))
        
        header.setLayout(header_layout)
        layout.addWidget(header)
        
        # スキルレベル設定エリア
        skills_frame = QFrame()
        skills_frame.setFrameStyle(QFrame.StyledPanel)
        skills_layout = QVBoxLayout()
        
        try:
            skills = self._db.get_skills(self._category_name, self._group_name)
            for skill in skills:
                skill_layout = QHBoxLayout()
                skill_layout.addWidget(QLabel(skill))
                
                level_combo = QComboBox()
                level_combo.addItems([str(i) for i in range(1, 6)])
                skill_layout.addWidget(level_combo)
                
                skills_layout.addLayout(skill_layout)
            
            skills_frame.setLayout(skills_layout)
            layout.addWidget(skills_frame)
            
        except Exception as e:
            self.logger.exception("スキルの読み込みに失敗しました")
            error_label = QLabel(f"スキルの読み込みに失敗しました: {str(e)}")
            error_label.setStyleSheet("color: red;")
            layout.addWidget(error_label)
        
        # レーダーチャートのプレースホルダー
        chart_frame = QFrame()
        chart_frame.setFrameStyle(QFrame.StyledPanel)
        chart_frame.setMinimumHeight(300)
        layout.addWidget(chart_frame)
        
        self.setLayout(layout)
