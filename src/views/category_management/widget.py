"""カテゴリーウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QGroupBox,
    QPushButton, QFrame
)
from ...database.database_manager import DatabaseManager
from .radar_chart import RadarChartWidget

class CategoryWidget(QWidget):
    """カテゴリータブのメインウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, category_name: str):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._category_name = category_name
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # ユーザー情報（上部）
        user_frame = self._create_user_section()
        layout.addWidget(user_frame)
        
        # スキル評価（中部）
        skills_frame = self._create_skills_section()
        layout.addWidget(skills_frame)
        
        # レーダーチャート（下部）
        chart_frame = self._create_chart_section()
        layout.addWidget(chart_frame)
        
        self.setLayout(layout)

    def _create_user_section(self):
        """ユーザー情報セクションの作成"""
        frame = QFrame()
        layout = QHBoxLayout()
        
        name_label = QLabel("ユーザー名:")
        self.user_label = QLabel("未選択")
        
        layout.addWidget(name_label)
        layout.addWidget(self.user_label)
        layout.addStretch()
        
        frame.setLayout(layout)
        return frame

    def _create_skills_section(self):
        """スキル評価セクションの作成"""
        frame = QFrame()
        layout = QVBoxLayout()
        
        skills_group = QGroupBox("スキル評価")
        skills_layout = QVBoxLayout()
        
        # スキルリストの取得と表示
        self.skill_combos = {}
        skills = self._get_category_skills()
        
        for skill in skills:
            skill_layout = QHBoxLayout()
            
            label = QLabel(skill)
            combo = QComboBox()
            combo.addItems(['1', '2', '3', '4', '5'])
            
            skill_layout.addWidget(label)
            skill_layout.addWidget(combo)
            
            self.skill_combos[skill] = combo
            skills_layout.addLayout(skill_layout)
        
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)
        
        frame.setLayout(layout)
        return frame

    def _create_chart_section(self):
        """レーダーチャートセクションの作成"""
        frame = QFrame()
        layout = QVBoxLayout()
        
        self.radar_chart = RadarChartWidget()
        layout.addWidget(self.radar_chart)
        
        frame.setLayout(layout)
        return frame

    def _get_category_skills(self):
        """カテゴリーのスキルリストを取得"""
        try:
            # TODO: データベースからスキルリストを取得
            return ["スキル1", "スキル2", "スキル3"]  # 仮のデータ
        except Exception as e:
            self.logger.exception("スキルリスト取得エラー")
            return []

    def update_user_data(self, user_name: str):
        """ユーザーデータの更新"""
        try:
            self.user_label.setText(user_name)
            
            # スキルレベルの更新
            skills = self._get_user_skills(user_name)
            for skill, level in skills.items():
                if skill in self.skill_combos:
                    self.skill_combos[skill].setCurrentText(str(level))
            
            self._update_chart()
            
        except Exception as e:
            self.logger.exception("ユーザーデータ更新エラー")

    def _get_user_skills(self, user_name: str):
        """ユーザーのスキルレベルを取得"""
        try:
            # TODO: データベースからユーザーのスキルレベルを取得
            return {
                "スキル1": 3,
                "スキル2": 4,
                "スキル3": 2
            }  # 仮のデータ
        except Exception as e:
            self.logger.exception("スキルレベル取得エラー")
            return {}

    def _update_chart(self):
        """レーダーチャートの更新"""
        try:
            data = {}
            for skill, combo in self.skill_combos.items():
                data[skill] = int(combo.currentText())
            
            self.radar_chart.update_data(data)
            
        except Exception as e:
            self.logger.exception("チャート更新エラー")
