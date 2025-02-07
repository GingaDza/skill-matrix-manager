import pytest
from PyQt6.QtWidgets import QApplication
from src.views.dialogs.category_dialog import CategoryDialog

@pytest.fixture
def app():
    """テスト用のQApplicationインスタンス"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def dialog(app):
    """テスト用のCategoryDialogインスタンス"""
    return CategoryDialog()

def test_initial_state(dialog):
    """初期状態のテスト"""
    assert dialog.windowTitle() == "カテゴリー設定"
    assert dialog.name_edit.text() == ""
    assert dialog.desc_edit.text() == ""
    assert dialog.parent_combo.currentData() is None

def test_load_category_data(app):
    """既存データ読み込みのテスト"""
    test_data = {
        'id': 1,
        'name': 'テストカテゴリー',
        'description': 'テスト用カテゴリーです',
        'parent_id': None
    }
    dialog = CategoryDialog(category_data=test_data)
    assert dialog.name_edit.text() == 'テストカテゴリー'
    assert dialog.desc_edit.text() == 'テスト用カテゴリーです'
    assert dialog.parent_combo.currentData() is None

def test_get_category_data(dialog):
    """入力データ取得のテスト"""
    dialog.name_edit.setText("新規カテゴリー")
    dialog.desc_edit.setText("新規カテゴリーの説明")
    
    data = dialog.get_category_data()
    assert data['id'] is None
    assert data['name'] == "新規カテゴリー"
    assert data['description'] == "新規カテゴリーの説明"
    assert data['parent_id'] is None

def test_circular_reference_check(app):
    """循環参照チェックのテスト"""
    categories = [
        {'id': 1, 'name': 'Category 1', 'parent_id': None},
        {'id': 2, 'name': 'Category 2', 'parent_id': 1},
        {'id': 3, 'name': 'Category 3', 'parent_id': 2}
    ]
    
    # Category 1を編集して、親をCategory 3にしようとする
    test_data = {'id': 1, 'name': 'Category 1', 'parent_id': None}
    dialog = CategoryDialog(category_data=test_data, categories=categories)
    
    # Category 3を親として選択
    index = dialog.parent_combo.findData(3)
    dialog.parent_combo.setCurrentIndex(index)
    
    assert dialog._has_circular_reference(1, 3) == True
