from PyQt6.QtWidgets import QTabWidget
import logging

class RightPane(QTabWidget):
    """右ペインコンポーネント"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        # 今後タブの追加などを実装
        pass
