from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SystemManagementTab(QWidget):
    """システム管理タブ"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """UIの設定"""
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("システム管理"))
