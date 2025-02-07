import sys
import pytest
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow

@pytest.fixture
def app():
    """テスト用のQApplicationインスタンス"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def main_window(app):
    """メインウィンドウのインスタンス"""
    window = MainWindow()
    yield window
    window.close()

def test_window_title(main_window):
    """ウィンドウタイトルのテスト"""
    assert "スキルマトリックス管理システム" == main_window.windowTitle()
