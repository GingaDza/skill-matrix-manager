import pytest
from PyQt6.QtWidgets import QApplication
from src.views.dialogs.skill_dialog import SkillDialog

@pytest.fixture
def app():
    """テスト用のQApplicationインスタンス"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def categories():
    """テスト用のカテゴリーリスト"""
    return [
        {'id': 1, 'name': 'プログラミング'},
        {'id': 2, 'name': 'データベース'},
        {'id': 3, 'name': 'インフラ'}
    ]

@pytest.fixture
def dialog(app, categories):
    """テスト用のSkillDialogインスタンス"""
    return SkillDialog(categories=categories)

def test_initial_state(dialog):
    """初期状態のテスト"""
    assert dialog.windowTitle() == "スキル設定"
    assert dialog.name_edit.text() == ""
    assert dialog.desc_edit.toPlainText() == ""
    assert dialog.level_spin.value() == 5
    assert len(dialog.level_desc_edits) == 5

def test_load_skill_data(app, categories):
    """既存データ読み込みのテスト"""
    test_data = {
        'id': 1,
        'name': 'Python',
        'description': 'Pythonプログラミング',
        'category_id': 1,
        'max_level': 3,
        'level_descriptions': {
            1: '基本構文の理解',
            2: '実践的なコーディング',
            3: 'フレームワークの活用'
        }
    }
    dialog = SkillDialog(categories=categories, skill_data=test_data)
    
    assert dialog.name_edit.text() == 'Python'
    assert dialog.desc_edit.toPlainText() == 'Pythonプログラミング'
    assert dialog.category_combo.currentData() == 1
    assert dialog.level_spin.value() == 3
    assert len(dialog.level_desc_edits) == 3
    assert dialog.level_desc_edits[0].text() == '基本構文の理解'
    assert dialog.level_desc_edits[1].text() == '実践的なコーディング'
    assert dialog.level_desc_edits[2].text() == 'フレームワークの活用'

def test_get_skill_data(dialog):
    """入力データ取得のテスト"""
    dialog.name_edit.setText("新規スキル")
    dialog.desc_edit.setPlainText("新規スキルの説明")
    dialog.category_combo.setCurrentIndex(0)
    dialog.level_spin.setValue(2)
    
    dialog.level_desc_edits[0].setText("レベル1の説明")
    dialog.level_desc_edits[1].setText("レベル2の説明")
    
    data = dialog.get_skill_data()
    assert data['id'] is None
    assert data['name'] == "新規スキル"
    assert data['description'] == "新規スキルの説明"
    assert data['category_id'] == 1
    assert data['max_level'] == 2
    assert data['level_descriptions'] == {
        1: "レベル1の説明",
        2: "レベル2の説明"
    }

def test_level_descriptions_update(dialog):
    """レベル説明フィールドの更新テスト"""
    initial_count = len(dialog.level_desc_edits)
    assert initial_count == 5
    
    # レベル数を変更
    dialog.level_spin.setValue(3)
    assert len(dialog.level_desc_edits) == 3
    
    # 説明を入力
    dialog.level_desc_edits[0].setText("レベル1")
    dialog.level_desc_edits[1].setText("レベル2")
    dialog.level_desc_edits[2].setText("レベル3")
    
    # レベル数を増やす
    dialog.level_spin.setValue(4)
    assert len(dialog.level_desc_edits) == 4
    
    # 既存の説明が保持されているか確認
    assert dialog.level_desc_edits[0].text() == "レベル1"
    assert dialog.level_desc_edits[1].text() == "レベル2"
    assert dialog.level_desc_edits[2].text() == "レベル3"
    assert dialog.level_desc_edits[3].text() == ""
