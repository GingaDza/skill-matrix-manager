"""データ入出力ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QPushButton, QFileDialog
)
from ...database.database_manager import DatabaseManager

class IOWidget(QWidget):
    """データ入出力タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # インポート
        import_group = QGroupBox("データインポート")
        import_layout = QVBoxLayout()
        
        group_import_btn = QPushButton("グループリストのインポート")
        category_import_btn = QPushButton("カテゴリーリストのインポート")
        skill_import_btn = QPushButton("スキルデータのインポート")
        
        import_layout.addWidget(group_import_btn)
        import_layout.addWidget(category_import_btn)
        import_layout.addWidget(skill_import_btn)
        
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        # アウトプット
        output_group = QGroupBox("データ出力")
        output_layout = QVBoxLayout()
        
        chart_export_btn = QPushButton("レーダーチャート一覧出力")
        pdf_export_btn = QPushButton("PDF出力")
        
        output_layout.addWidget(chart_export_btn)
        output_layout.addWidget(pdf_export_btn)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        self.setLayout(layout)
