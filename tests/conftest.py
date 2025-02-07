import pytest
from PyQt6.QtWidgets import QApplication
import sys

@pytest.fixture(scope="session")
def qapp():
    """グローバルなQApplicationインスタンス"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
