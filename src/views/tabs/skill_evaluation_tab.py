from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from datetime import datetime
# 相対インポートを絶対インポートに変更
from desktop.utils.time_utils import TimeProvider
from desktop.controllers.skill_controller import SkillController
import logging

logger = logging.getLogger(__name__)

class SkillEvaluationTab(QWidget):
    def __init__(self, controllers):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime(2025, 2, 3, 9, 5, 7)
        self.current_user = "GingaDza"
        
        self.init_ui()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            layout = QVBoxLayout(self)
            
            # 仮のラベル
            layout.addWidget(QLabel("スキル評価タブ"))
            
            logger.debug(f"{self.current_time} - {self.current_user} initialized SkillEvaluationTab UI")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to initialize SkillEvaluationTab UI: {str(e)}")
            raise