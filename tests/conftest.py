"""テスト用の共通フィクスチャ"""
import pytest
from PyQt5.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """PyQtアプリケーションのフィクスチャ"""
    app = QApplication([])
    yield app
    app.quit()
