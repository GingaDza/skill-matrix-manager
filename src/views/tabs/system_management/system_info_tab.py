from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextBrowser
)
from PyQt6.QtCore import Qt, QT_VERSION_STR
from PyQt6 import QtCore
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
        <p>Python: {sys.version.split()[0]}</p>
        <p>PyQt: {QT_VERSION_STR}</p>
        <p>Qt: {QtCore.qVersion()}</p>
        
        <h3>データベース情報</h3>
        <p>種類: SQLite</p>
        <p>場所: data/skill_matrix.db</p>
        
        <h3>機能一覧</h3>
        <ul>
            <li>グループ管理
                <ul>
                    <li>グループの作成・編集・削除</li>
                    <li>ユーザーのグループ割り当て</li>
                </ul>
            </li>
            <li>カテゴリー管理
                <ul>
                    <li>カテゴリーの作成・編集・削除</li>
                    <li>スキル項目の管理</li>
                </ul>
            </li>
            <li>スキル評価
                <ul>
                    <li>ユーザーごとのスキル評価入力</li>
                    <li>レーダーチャートによる可視化</li>
                </ul>
            </li>
            <li>データ管理
                <ul>
                    <li>Excel/CSVインポート・エクスポート</li>
                    <li>PDF出力機能</li>
                </ul>
            </li>
        </ul>

        <h3>ショートカットキー</h3>
        <table>
            <tr><td>Ctrl+N</td><td>新規作成</td></tr>
            <tr><td>Ctrl+S</td><td>保存</td></tr>
            <tr><td>Ctrl+P</td><td>印刷</td></tr>
            <tr><td>Ctrl+Q</td><td>アプリケーション終了</td></tr>
        </table>
        
        <h3>サポート情報</h3>
        <p>不具合報告や機能要望は以下までお願いします：</p>
        <p><a href="mailto:support@example.com">support@example.com</a></p>
        
        <h3>更新履歴</h3>
        <p>Version 1.0.0 (2025-02-07)</p>
        <ul>
            <li>初期リリース</li>
            <li>基本機能の実装</li>
            <li>グループ管理機能の追加</li>
            <li>カテゴリー管理機能の追加</li>
        </ul>
        """
        
        info_browser.setHtml(system_info)
        layout.addWidget(info_browser)
