"""評価タブモジュール"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QFrame, QPushButton
)
from ...database.database_manager import DatabaseManager
from ..charts.radar_chart import RadarChart

class EvaluationTab(QWidget):
    """評価タブクラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # グループ選択セクション
        group_section = QFrame()
        group_layout = QHBoxLayout()
        
        group_label = QLabel("グループ:")
        self.group_combo = QComboBox()
        self.group_combo.currentTextChanged.connect(self._update_charts)
        
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)
        group_layout.addStretch()
        
        group_section.setLayout(group_layout)
        layout.addWidget(group_section)
        
        # チャート表示セクション
        charts_section = QFrame()
        charts_layout = QHBoxLayout()
        
        # 個人レーダーチャート
        individual_chart = RadarChart()
        charts_layout.addWidget(individual_chart)
        
        # グループ平均レーダーチャート
        group_chart = RadarChart()
        charts_layout.addWidget(group_chart)
        
        charts_section.setLayout(charts_layout)
        layout.addWidget(charts_section)
        
        # 統計情報セクション
        stats_section = QFrame()
        stats_layout = QVBoxLayout()
        
        self.stats_label = QLabel()
        stats_layout.addWidget(self.stats_label)
        
        stats_section.setLayout(stats_layout)
        layout.addWidget(stats_section)
        
        # エクスポートセクション
        export_section = QFrame()
        export_layout = QHBoxLayout()
        
        export_btn = QPushButton("PDFエクスポート")
        export_btn.clicked.connect(self._export_pdf)
        
        export_layout.addStretch()
        export_layout.addWidget(export_btn)
        
        export_section.setLayout(export_layout)
        layout.addWidget(export_section)
        
        self.setLayout(layout)
        self._load_groups()

    def _load_groups(self):
        """グループデータの読み込み"""
        try:
            groups = self._db_manager.get_groups()
            self.group_combo.clear()
            self.group_combo.addItems(groups)
            
        except Exception as e:
            self.logger.exception("グループデータ読み込みエラー")

    def _update_charts(self):
        """チャートの更新"""
        try:
            current_group = self.group_combo.currentText()
            if not current_group:
                return
                
            # データの取得と更新
            group_data = self._db_manager.get_group_skills(current_group)
            
            # TODO: チャートの更新処理
            
            # 統計情報の更新
            self._update_stats(group_data)
            
        except Exception as e:
            self.logger.exception("チャート更新エラー")

    def _update_stats(self, group_data: dict):
        """統計情報の更新"""
        try:
            # TODO: 統計情報の計算と表示
            pass
            
        except Exception as e:
            self.logger.exception("統計情報更新エラー")

    def _export_pdf(self):
        """PDF出力"""
        try:
            # TODO: PDF出力処理
            pass
            
        except Exception as e:
            self.logger.exception("PDF出力エラー")

