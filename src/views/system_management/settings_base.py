"""設定ウィジェットの基本クラス"""
from typing import Optional
from PyQt6.QtWidgets import QWidget
from ..base.base_widget import BaseWidget
from .group_manager import GroupManagerMixin
from .category_manager import CategoryManagerMixin
from .skill_manager import SkillManagerMixin

class SettingsWidgetBase(BaseWidget, GroupManagerMixin, CategoryManagerMixin, SkillManagerMixin):
    """設定ウィジェットの基本クラス"""
    
    def __init__(self, db_manager, parent: Optional[QWidget] = None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャー
            parent: 親ウィジェット
        """
        super().__init__(db_manager=db_manager, parent=parent)
        self.logger.info("SettingsWidgetBase initialized")

    def _on_group_selected(self, row: int):
        """グループ選択時のイベント"""
        try:
            group_item = self.category_group_combo.itemText(row)
            self.logger.info(f"グループ選択: {group_item}")
            
            # グループ選択を同期
            self._on_category_group_changed(row)
            
            # カテゴリー一覧を取得して最上位を選択
            categories = self._db_manager.get_categories_by_group(group_item)
            if categories:
                self.parent_list.setCurrentRow(0)  # 最上位のカテゴリーを選択
                self._on_parent_selected(0)  # カテゴリー選択時の処理を実行
                
                # スキル一覧を取得して最上位を選択
                skills = self._db_manager.get_skills_by_parent(categories[0])
                if skills:
                    self.child_list.setCurrentRow(0)  # 最上位のスキルを選択
                
        except Exception as e:
            self.logger.exception("グループ選択エラー")

    def _on_parent_selected(self, row: int):
        """カテゴリー選択時のイベント"""
        try:
            if row >= 0:
                parent_item = self.parent_list.item(row)
                if parent_item:
                    parent_name = parent_item.text()
                    group_name = self.category_group_combo.currentText()
                    self.logger.info(f"選択されたカテゴリー: {parent_name}, グループ: {group_name}")
                    
                    # スキル一覧を取得して最上位を選択
                    skills = self._db_manager.get_skills_by_parent(parent_name)
                    self.logger.info(f"カテゴリーのスキル: {skills}")
                    
                    self.child_list.clear()
                    self.child_list.addItems(skills)
                    
                    if skills:
                        self.child_list.setCurrentRow(0)  # 最上位のスキルを選択
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    # ... (残りのメソッドは変更なし)
