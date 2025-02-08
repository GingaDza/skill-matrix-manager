"""マイグレーションコマンド"""
import os
import sys
import importlib.util
import logging
from typing import List
from pathlib import Path
from ..database.migrations.migration_manager import MigrationManager
from ..utils.display import display

def get_migration_files() -> List[tuple]:
    """マイグレーションファイルの一覧を取得"""
    migrations_dir = Path(__file__).parent.parent / "database" / "migrations"
    migration_files = []
    
    for file in migrations_dir.glob("V*__.py"):
        if file.name.startswith("V") and file.name.endswith(".py"):
            module_name = file.stem
            version = module_name.split("__")[0]
            migration_files.append((version, file))
    
    return sorted(migration_files)

def run_migrations(db_path: str):
    """マイグレーションを実行"""
    display.show_section("データベースマイグレーション")
    
    # データベースディレクトリを作成
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    manager = MigrationManager(db_path)
    applied = manager.get_applied_migrations()
    
    migration_files = get_migration_files()
    if not migration_files:
        display.show_message("適用可能なマイグレーションが見つかりません", "warning")
        return
    
    display.show_message(f"検出されたマイグレーション: {[v for v, _ in migration_files]}", "info")
    
    for version, file in migration_files:
        if version in applied:
            display.show_message(f"マイグレーション {version} は既に適用済みです", "info")
            continue
        
        try:
            # モジュールを動的にインポート
            spec = importlib.util.spec_from_file_location(f"migrations.{file.stem}", file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # マイグレーションを適用
            display.show_message(f"マイグレーション {version} を適用中: {module.NAME}", "info")
            manager.apply_migration(version, module.NAME, module.up())
            display.show_message(f"マイグレーション {version} の適用が完了しました", "success")
        
        except Exception as e:
            display.show_message(f"マイグレーション {version} の適用に失敗しました: {e}", "error")
            sys.exit(1)

def rollback_migration(db_path: str, version: str):
    """マイグレーションをロールバック"""
    display.show_section(f"マイグレーション {version} のロールバック")
    
    if not os.path.exists(db_path):
        display.show_message("データベースファイルが存在しません", "error")
        sys.exit(1)
    
    manager = MigrationManager(db_path)
    applied = manager.get_applied_migrations()
    
    if version not in applied:
        display.show_message(f"マイグレーション {version} は適用されていません", "warning")
        return
    
    try:
        migrations_dir = Path(__file__).parent.parent / "database" / "migrations"
        file = next(migrations_dir.glob(f"{version}__.py"))
        
        # モジュールを動的にインポート
        spec = importlib.util.spec_from_file_location(f"migrations.{file.stem}", file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # ロールバックを実行
        display.show_message(f"マイグレーション {version} をロールバック中", "info")
        manager.rollback_migration(version, module.down())
        display.show_message(f"マイグレーション {version} のロールバックが完了しました", "success")
    
    except Exception as e:
        display.show_message(f"マイグレーション {version} のロールバックに失敗しました: {e}", "error")
        sys.exit(1)
