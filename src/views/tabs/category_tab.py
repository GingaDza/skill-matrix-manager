"""カテゴリータブモジュール"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QFrame, QGridLayout
)
from ...database.database_manager import DatabaseManager
from ..charts.radar_chart import RadarChart

class CategoryTab(QWidget):
    """カテゴリータブクラス"""
    
    def __init__(self, db_manager: DatabaseManager, category_name: str):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._category_name = category_name
        
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # ユーザー情報セクション（上部）
        user_section = QFrame()
        user_layout = QHBoxLayout()
        
        user_label = QLabel("ユーザー名:")
        self.user_label = QLabel("未選択")
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_label)
        user_layout.addStretch()
        
        user_section.setLayout(user_layout)
        layout.addWidget(user_section)
        
        # スキル評価セクション（中部）
        skills_section = QFrame()
        skills_layout = QGridLayout()
        
        # スキルリストの取得と表示
        skills = self._db_manager.get_skills_by_category(self._category_name)
        self.skill_combos = {}
        
        for i, skill in enumerate(skills):
            label = QLabel(skill)
            combo = QComboBox()
            combo.addItems(['1', '2', '3', '4', '5'])
            
            skills_layout.addWidget(label, i, 0)
            skills_layout.addWidget(combo, i, 1)
            self.skill_combos[skill] = combo
        
        skills_section.setLayout(skills_layout)
        layout.addWidget(skills_section)
        
        # レーダーチャートセクション（下部）
        chart_section = QFrame()
        chart_layout = QVBoxLayout()
        
        self.radar_chart = RadarChart()
        chart_layout.addWidget(self.radar_chart)
        
        chart_section.setLayout(chart_layout)
        layout.addWidget(chart_section)
        
        self.setLayout(layout)
        
    def update_user_data(self, user_name: str):
        """ユーザーデータの更新"""
        try:
            self.user_label.setText(user_name)
            
            # スキルレベルの取得と設定
            skills = self._db_manager.get_user_skills(
                user_name,
                self._category_name
            )
            
            for skill, level in skills.items():
                if skill in self.skill_combos:
                    self.skill_combos[skill].setCurrentText(str(level))
            
            # レーダーチャートの更新
            self._update_radar_chart()
            
        except Exception as e:
            self.logger.exception(f"ユーザーデータ更新エラー: {user_name}")
            
    def _update_radar_chart(self):
        """レーダーチャートの更新"""
        try:
            data = {}
            for skill, combo in self.skill_combos.items():
                data[skill] = int(combo.currentText())
            
            self.radar_chart.update_data(data)
            
        except Exception as e:
            self.logger.exception("レーダーチャート更新エラー")

