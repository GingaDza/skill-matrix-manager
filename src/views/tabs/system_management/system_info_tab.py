from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextBrowser
)
from PyQt6.QtCore import Qt
import platform
import sys

class SystemInfoTab(QWidget):
    """システム情報タブ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """UIの設定"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # システム情報の表示
        title = QLabel("システム情報")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        info_browser = QTextBrowser()
        info_browser.setOpenExternalLinks(True)
        
        system_info = f"""
        <h3>アプリケーション情報</h3>
        <p>バージョン: 1.0.0</p>
        <p>作成日: 2025-02-07</p>
        
        <h3>システム情報</h3>
        <p>OS: {platform.system()} {platform.release()}</p>
        <p>Python: {sys.version}</p>
        <p>PyQt: {Qt.qVersion()}</p>
        
        <h3>データベース情報</h3>
        <p>種類: SQLite</p>
        <p>場所: data/skill_matrix.db</p>
        
        <h3>使用方法</h3>
        <p>1. システム管理タブでグループとカテゴリーを設定</p>
        <p>2. ユーザーを追加し、グループに割り当て</p>
        <p>3. スキル評価を入力</p>
        <p>4. 総合評価タブで結果を確認</p>
        
        <h3>サポート</h3>
        <p>不具合報告や機能要望は以下までお願いします：</p>
        <p><a href="mailto:support@example.com">support@example.com</a></p>
        """
        
        info_browser.setHtml(system_info)
        layout.addWidget(info_browser)
