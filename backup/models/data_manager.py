# src/desktop/models/data_manager.py
"""
Data manager implementation
Created: 2025-01-31 22:13:45
Author: GingaDza
"""
from PySide6.QtCore import QObject, Signal
from uuid import uuid4
from datetime import datetime
from .user import User
from .group import Group
from .category import Category
from .skill import Skill

class DataManager(QObject):
    # シグナル定義
    users_changed = Signal()
    groups_changed = Signal()
    categories_changed = Signal()
    skills_changed = Signal()
    
    def __init__(self):
        super().__init__()
        # データストア
        self.users = {}
        self.groups = {}
        self.categories = {}
        self.skills = {}
        
        # 現在のユーザー
        self._current_user_id = None
        
        # メタデータ
        self.created_at = datetime.utcnow()
        self.created_by = "GingaDza"
        self.last_modified_at = self.created_at
        self.last_modified_by = self.created_by
        
        # 初期データの作成
        self.create_initial_data()
    
    def create_initial_data(self):
        """初期データの作成"""
        try:
            # サンプルグループの作成
            group_id = self.create_group(
                name="開発チーム",
                description="ソフトウェア開発チーム"
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
                group_id=group_id
            )
            
            self.create_user(
                name="鈴木 花子",
                email="hanako.suzuki@example.com",
                group_id=group_id
            )
        
        except Exception as e:
            print(f"初期データの作成中にエラーが発生しました: {e}")
    
    @property
    def current_user_id(self) -> str:
        """現在選択中のユーザーID"""
        return self._current_user_id
    
    @current_user_id.setter
    def current_user_id(self, value: str):
        """現在のユーザーIDを設定"""
        if value and value not in self.users:
            raise ValueError("指定されたユーザーが存在しません")
        self._current_user_id = value
    
    def create_user(self, name: str, email: str, group_id: str = None) -> str:
        """新規ユーザーの作成"""
        # 入力検証
        if not name or not email:
            raise ValueError("名前とメールアドレスは必須です")
        
        # メールアドレスの重複チェック
        for user in self.users.values():
            if user.email == email:
                raise ValueError(f"メールアドレス {email} は既に使用されています")
        
        # グループの存在確認
        if group_id and group_id not in self.groups:
            raise ValueError("指定されたグループが存在しません")
        
        # ユーザーIDの生成
        user_id = str(uuid4())
        
        # ユーザーの作成
        user = User(
            id=user_id,
            name=name,
            email=email,
            group_id=group_id
        )
        
        # ユーザーの保存
        self.users[user_id] = user
        
        # グループにメンバーを追加
        if group_id:
            self.groups[group_id].add_member(user_id)
        
        # メタデータの更新
        self._update_modified()
        
        # 変更通知
        self.users_changed.emit()
        
        return user_id
    
    def create_group(self, name: str, description: str = "") -> str:
        """新規グループの作成"""
        # 入力検証
        if not name:
            raise ValueError("グループ名は必須です")
        
        # グループ名の重複チェック
        for group in self.groups.values():
            if group.name == name:
                raise ValueError(f"グループ名 {name} は既に使用されています")
        
        # グループIDの生成
        group_id = str(uuid4())
        
        # グループの作成
        group = Group(
            id=group_id,
            name=name,
            description=description
        )
        
        # グループの保存
        self.groups[group_id] = group
        
        # メタデータの更新
        self._update_modified()
        
        # 変更通知
        self.groups_changed.emit()
        
        return group_id
    
    def create_category(self, name: str, description: str = "") -> str:
        """新規カテゴリーの作成"""
        # 入力検証
        if not name:
            raise ValueError("カテゴリー名は必須です")
        
        # カテゴリー名の重複チェック
        for category in self.categories.values():
            if category.name == name:
                raise ValueError(f"カテゴリー名 {name} は既に使用されています")
        
        # カテゴリーIDの生成
        category_id = str(uuid4())
        
        # カテゴリーの作成
        category = Category(
            id=category_id,
            name=name,
            description=description
        )
        
        # カテゴリーの保存
        self.categories[category_id] = category
        
        # メタデータの更新
        self._update_modified()
        
        # 変更通知
        self.categories_changed.emit()
        
        return category_id
    
    def create_skill(self, name: str, category_id: str, description: str = "") -> str:
        """新規スキルの作成"""
        # 入力検証
        if not name:
            raise ValueError("スキル名は必須です")
        
        if not category_id or category_id not in self.categories:
            raise ValueError("有効なカテゴリーを指定してください")
        
        # スキル名の重複チェック（同じカテゴリー内で）
        for skill in self.skills.values():
            if skill.category_id == category_id and skill.name == name:
                raise ValueError(f"スキル名 {name} は既に使用されています")
        
        # スキルIDの生成
        skill_id = str(uuid4())
        
        # スキルの作成
        skill = Skill(
            id=skill_id,
            name=name,
            category_id=category_id,
            description=description
        )
        
        # スキルの保存
        self.skills[skill_id] = skill
        
        # カテゴリーにスキルを追加
        self.categories[category_id].add_skill(skill_id)
        
        # メタデータの更新
        self._update_modified()
        
        # 変更通知
        self.skills_changed.emit()
        
        return skill_id
    
    def get_group_users(self, group_id: str = None) -> list:
        """グループに属するユーザーの取得"""
        if not group_id:
            return sorted(
                self.users.values(),
                key=lambda x: x.name
            )
        
        if group_id not in self.groups:
            return []
        
        return sorted(
            [self.users[user_id] 
             for user_id in self.groups[group_id].members 
             if user_id in self.users],
            key=lambda x: x.name
        )
    
    def get_all_groups(self) -> list:
        """全グループ一覧を取得"""
        return sorted(
            self.groups.values(),
            key=lambda x: x.name
        )
    
    def get_group_categories(self, group_id: str = None) -> list:
        """カテゴリー一覧を取得"""
        return sorted(
            self.categories.values(),
            key=lambda x: x.name
        )
    
    def get_category_skills(self, category_id: str) -> list:
        """カテゴリーのスキル一覧を取得"""
        if not category_id:
            return []
        
        return sorted(
            [skill for skill in self.skills.values()
             if skill.category_id == category_id],
            key=lambda x: x.name
        )
    
    def delete_group(self, group_id: str):
        """グループの削除"""
        group = self.groups.get(group_id)
        if not group:
            raise ValueError("指定されたグループが存在しません")
        
        # メンバーのグループIDをクリア
        for user_id in group.members.copy():
            if user_id in self.users:
                self.users[user_id].group_id = None
        
        # グループの削除
        del self.groups[group_id]
        
        # メタデータの更新
        self._update_modified()
        
        # 変更通知
        self.groups_changed.emit()
        self.users_changed.emit()
    
    def _update_modified(self):
        """最終更新情報の更新"""
        self.last_modified_at = datetime.utcnow()
        self.last_modified_by = self.created_by

    # src/desktop/models/data_manager.py に追加

def delete_group(self, group_id: str):
    """グループの削除"""
    group = self.groups.get(group_id)
    if not group:
        raise ValueError("指定されたグループが存在しません")
    
    # メンバーのグループIDをクリア
    for user_id in group.members.copy():
        if user_id in self.users:
            self.users[user_id].group_id = None
    
    # グループの削除
    del self.groups[group_id]
    
    # メタデータの更新
    self._update_modified()
    
    # 変更通知
    self.groups_changed.emit()
    self.users_changed.emit()