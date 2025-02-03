from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .initial_settings.initial_settings_tab import InitialSettingsTab

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SystemManagementTab(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.current_time = datetime(2025, 2, 3, 10, 42, 50)
        self.current_user = "GingaDza"
        self.controllers = controllers
        
        logger.debug(f"{self.current_time} - {self.current_user} Initializing SystemManagementTab")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 内部タブウィジェット
        self.tab_widget = QTabWidget()
        
        # 初期設定タブ
        logger.debug(f"{self.current_time} - {self.current_user} Creating InitialSettingsTab")
        self.initial_settings_tab = InitialSettingsTab(self.controllers)
        self.tab_widget.addTab(self.initial_settings_tab, "初期設定")
        
        layout.addWidget(self.tab_widget)
        logger.debug(f"{self.current_time} - {self.current_user} SystemManagementTab UI setup completed")