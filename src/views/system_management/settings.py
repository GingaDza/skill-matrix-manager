"""設定ウィジェット"""
from typing import Optional
from PyQt6.QtWidgets import QWidget
from .settings_base import SettingsWidgetBase

class SettingsWidget(SettingsWidgetBase):
    """設定ウィジェット"""
    
    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャー
            parent: 親ウィジェット
        """
        super().__init__(db_manager=db_manager, parent=parent)
