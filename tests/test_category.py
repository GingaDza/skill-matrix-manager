import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.models import Category

def test_create_category(db: Session):
    """カテゴリーの作成をテスト"""
    # カテゴリーを作成
    category = Category(name="Original Name")
    db.add(category)
    db.commit()
    db.refresh(category)

    # 検証
    assert category.id is not None
    assert category.name == "Original Name"
    assert isinstance(category.created_at, datetime)
    assert isinstance(category.updated_at, datetime)

def test_create_category_without_description(db: Session):
    """説明なしでカテゴリーを作成するテスト"""
    category = Category(name="No Description")
    db.add(category)
    db.commit()
    db.refresh(category)

    assert category.id is not None
    assert category.name == "No Description"
    assert category.description is None

def test_create_category_with_parent(db: Session):
    """親カテゴリー付きでカテゴリーを作成するテスト"""
    # 親カテゴリーを作成
    parent = Category(name="Parent Category")
    db.add(parent)
    db.commit()
    db.refresh(parent)

    # 子カテゴリーを作成
    child = Category(
        name="Child Category",
        parent_id=parent.id
    )
    db.add(child)
    db.commit()
    db.refresh(child)

    # 検証
    assert child.parent_id == parent.id
    assert child.parent.name == "Parent Category"
    assert parent.children[0].name == "Child Category"

def test_update_category(db: Session):
    """カテゴリーの更新をテスト"""
    # カテゴリーを作成
    category = Category(name="Original Name")
    db.add(category)
    db.commit()
    db.refresh(category)

    # 更新前の時刻を保存
    original_created_at = category.created_at
    original_updated_at = category.updated_at

    # 少し待って更新
    category.name = "Updated Name"
    category.description = "Updated Description"
    db.commit()
    db.refresh(category)

    # 検証
    assert category.name == "Updated Name"
    assert category.description == "Updated Description"
    assert category.created_at == original_created_at
    assert category.updated_at > original_updated_at

def test_delete_category(db: Session):
    """カテゴリーの削除をテスト"""
    # カテゴリーを作成
    category = Category(name="To Delete")
    db.add(category)
    db.commit()
    db.refresh(category)

    # IDを保存
    category_id = category.id

    # 削除
    db.delete(category)
    db.commit()

    # 検証
    deleted_category = db.query(Category).filter(Category.id == category_id).first()
    assert deleted_category is None

def test_duplicate_category_name(db: Session):
    """カテゴリー名の重複をテスト"""
    # 最初のカテゴリーを作成
    category1 = Category(name="Duplicate Name")
    db.add(category1)
    db.commit()

    # 同じ名前で2つ目のカテゴリーを作成
    category2 = Category(name="Duplicate Name")
    db.add(category2)
    
    # 重複エラーを検証
    with pytest.raises(IntegrityError):
        db.commit()

def test_category_relationships(db: Session):
    """カテゴリーの関係性をテスト"""
    # 親カテゴリーを作成
    parent = Category(name="Parent")
    db.add(parent)
    db.commit()
    db.refresh(parent)

    # 複数の子カテゴリーを作成
    child1 = Category(name="Child 1", parent_id=parent.id)
    child2 = Category(name="Child 2", parent_id=parent.id)
    db.add(child1)
    db.add(child2)
    db.commit()

    # リレーションシップを検証
    assert len(parent.children) == 2
    assert parent.children[0].name in ["Child 1", "Child 2"]
    assert parent.children[1].name in ["Child 1", "Child 2"]
    assert child1.parent.id == parent.id
    assert child2.parent.id == parent.id

@pytest.fixture(autouse=True)
def setup_test(db: Session):
    """各テスト前の準備"""
    yield
    # テスト後のクリーンアップ
    try:
        db.query(Category).delete()
        db.commit()
    except:
        db.rollback()