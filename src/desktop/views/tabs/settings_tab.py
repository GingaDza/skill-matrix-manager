from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from datetime import datetime
# 絶対インポートを使用
from desktop.controllers.skill_controller import SkillController
import logging

logger = logging.getLogger(__name__)

class SettingsTab(QWidget):
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
            layout.addWidget(QLabel("設定タブ"))
            
            logger.debug(f"{self.current_time} - {self.current_user} initialized SettingsTab UI")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to initialize SettingsTab UI: {str(e)}")
            raise