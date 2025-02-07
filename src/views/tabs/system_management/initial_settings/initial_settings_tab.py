from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from .sections.category.category_section import CategorySection
from .sections.group_section import GroupSection
import logging
from datetime import datetime

class InitialSettingsTab(QWidget):
    """初期設定タブ
    
    グループとカテゴリーの管理を行うタブ。
    スクロール可能なレイアウトで、グループセクションとカテゴリーセクションを含む。
    
    Attributes:
        current_time (datetime): 現在の時刻
        current_user (str): 現在のユーザー名
        group_section (GroupSection): グループ管理セクション
        category_section (CategorySection): カテゴリー管理セクション
    """
    
    def __init__(self, parent=None):
        """初期化
        
        Args:
            parent (QWidget, optional): 親ウィジェット. Defaults to None.
        """
        super().__init__(parent)
        self.current_time = datetime(2025, 2, 3, 19, 19, 42)
        self.current_user = "GingaDza"
        self.setup_logging()
        self.setup_ui()
        logging.info(f"{self.current_time} - {self.current_user} InitialSettingsTab initialized")

    def setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('initial_settings.log')
            ]
        )
        logging.info(f"{self.current_time} - {self.current_user} Logging setup completed")

    def setup_ui(self):
        """UIの設定
        
        スクロール可能なメインレイアウトを作成し、
        グループセクションとカテゴリーセクションを配置する。
        """
        try:
            logging.debug(f"{self.current_time} - {self.current_user} Setting up UI")
            
            # メインレイアウト
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            
            # スクロールエリア
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setMinimumWidth(800)  # 最小幅を設定
            scroll.setMinimumHeight(600)  # 最小高さを設定
            
            # スクロールの内容となるウィジェット
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setSpacing(20)  # セクション間のスペースを設定
            
            # グループセクション
            self.group_section = GroupSection(self)
            scroll_layout.addWidget(self.group_section)
            logging.debug(f"{self.current_time} - {self.current_user} Group section added")
            
            # カテゴリーセクション
            self.category_section = CategorySection(self)
            scroll_layout.addWidget(self.category_section)
            logging.debug(f"{self.current_time} - {self.current_user} Category section added")
            
            # スペーサーを追加
            scroll_layout.addStretch()
            
            # スクロールエリアにウィジェットを設定
            scroll.setWidget(scroll_content)
            
            # メインレイアウトにスクロールエリアを追加
            main_layout.addWidget(scroll)
            
            # グループセクションのシグナルを接続
            self.group_section.group_selected.connect(self.handle_group_selection)
            logging.debug(f"{self.current_time} - {self.current_user} Group selection signal connected")
            
            logging.info(f"{self.current_time} - {self.current_user} UI setup completed")
            
        except Exception as e:
            logging.error(f"{self.current_time} - {self.current_user} Error in UI setup: {str(e)}")
            logging.exception("Detailed traceback:")

    def handle_group_selection(self, group_name):
        """グループ選択時の処理
        
        Args:
            group_name (str): 選択されたグループ名
        """
        try:
            logging.debug(f"{self.current_time} - {self.current_user} Handling group selection: {group_name}")
            
            # カテゴリーセクションに選択されたグループを設定
            if self.category_section:
                self.category_section.set_selected_group(group_name)
                logging.info(f"{self.current_time} - {self.current_user} Group {group_name} set in category section")
            else:
                logging.warning(f"{self.current_time} - {self.current_user} Category section not initialized")
                
        except Exception as e:
            logging.error(f"{self.current_time} - {self.current_user} Error handling group selection: {str(e)}")
            logging.exception("Detailed traceback:")

    def cleanup(self):
        """クリーンアップ処理
        
        タブが閉じられる際のリソース解放処理
        """
        try:
            logging.debug(f"{self.current_time} - {self.current_user} Starting cleanup")
            
            # グループセクションのクリーンアップ
            if hasattr(self, 'group_section'):
                self.group_section.cleanup()
                logging.debug(f"{self.current_time} - {self.current_user} Group section cleanup completed")
            
            # カテゴリーセクションのクリーンアップ
            if hasattr(self, 'category_section'):
                self.category_section.cleanup()
                logging.debug(f"{self.current_time} - {self.current_user} Category section cleanup completed")
                
            logging.info(f"{self.current_time} - {self.current_user} Cleanup completed")
            
        except Exception as e:
            logging.error(f"{self.current_time} - {self.current_user} Error during cleanup: {str(e)}")
            logging.exception("Detailed traceback:")

    def resizeEvent(self, event):
        """リサイズイベントハンドラ
        
        Args:
            event (QResizeEvent): リサイズイベント
        """
        try:
            super().resizeEvent(event)
            logging.debug(f"{self.current_time} - {self.current_user} Window resized to {event.size().width()}x{event.size().height()}")
        except Exception as e:
            logging.error(f"{self.current_time} - {self.current_user} Error handling resize event: {str(e)}")
            logging.exception("Detailed traceback:")

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = InitialSettingsTab()
    window.show()
    sys.exit(app.exec())