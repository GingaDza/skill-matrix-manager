from PyQt6.QtWidgets import QTabWidget
from .group_manager import GroupManager
import logging

class SystemManagementTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """UIの初期設定"""
        # 初期設定タブ
        self.group_manager = GroupManager(self)
        self.addTab(self.group_manager, "初期設定")

        # データ入出力タブ
        # self.io_tab = DataIOTab(self)
        # self.addTab(self.io_tab, "データ入出力")

        # システム情報タブ
        # self.info_tab = SystemInfoTab(self)
        # self.addTab(self.info_tab, "システム情報")

    def load_data(self):
        """データの読み込み"""
        try:
            self.group_manager.load_groups()
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
