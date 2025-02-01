# src/desktop/models/data_manager/manager.py
"""
Main data manager implementation
Created: 2025-01-31 22:32:29
Author: GingaDza
"""
from .group import GroupManager
from .user import UserManager
from .skill import SkillManager

class DataManager(GroupManager, UserManager, SkillManager):
    def __init__(self):
        super().__init__()
        self.create_initial_data()
    
    def create_initial_data(self):
        """初期データの作成"""
        try:
            # サンプルグループの作成
            dev_team_id = self.create_group(
                name="開発チーム",
                description="ソフトウェア開発チーム"
            )
            
            test_team_id = self.create_group(
                name="テストチーム",
                description="品質保証チーム"
            )
            
            # サンプルカテゴリーの作成
            programming_id = self.create_category(
                name="プログラミング",
                description="プログラミング言語とフレームワーク"
            )
            
            tools_id = self.create_category(
                name="開発ツール",
                description="開発支援ツールとミドルウェア"
            )
            
            # サンプルスキルの作成
            self.create_skill(
                name="Python",
                category_id=programming_id,
                description="Pythonプログラミング"
            )
            
            self.create_skill(
                name="Git",
                category_id=tools_id,
                description="バージョン管理システム"
            )
            
            # サンプルユーザーの作成
            self.create_user(
                name="山田 太郎",
                email="taro.yamada@example.com",
                group_id=dev_team_id
            )
            
            self.create_user(
                name="鈴木 花子",
                email="hanako.suzuki@example.com",
                group_id=test_team_id
            )
            
        except Exception as e:
            print(f"初期データの作成中にエラーが発生しました: {e}")