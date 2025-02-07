import sys
import pytest
from PyQt6.QtWidgets import QApplication
from src.views.dialogs.group_dialog import GroupDialog

@pytest.fixture
def app():
    """テスト用のQApplicationインスタンス"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def dialog(app):
    """テスト用のGroupDialogインスタンス"""
    return GroupDialog()

def test_initial_state(dialog):
    """初期状態のテスト"""
    assert dialog.windowTitle() == "グループ設定"
    assert dialog.name_edit.text() == ""
    assert dialog.desc_edit.text() == ""

def test_load_group_data(app):
    """既存データ読み込みのテスト"""
    test_data = {
        'id': 1,
        'name': 'テストグループ',
        'description': 'テスト用グループです'
    }
    dialog = GroupDialog(group_data=test_data)
    assert dialog.name_edit.text() == 'テストグループ'
    assert dialog.desc_edit.text() == 'テスト用グループです'

def test_get_group_data(dialog):
    """入力データ取得のテスト"""
    dialog.name_edit.setText("新規グループ")
    dialog.desc_edit.setText("新規グループの説明")
    
    data = dialog.get_group_data()
    assert data['id'] is None
    assert data['name'] == "新規グループ"
    assert data['description'] == "新規グループの説明"
