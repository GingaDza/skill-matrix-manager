            items = self.group_list.findItems(group_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.group_list.setCurrentItem(items[0])
            
            # グループコンボボックスの選択を同期
            index = self.category_group_combo.findText(group_name)
            if index >= 0:
                self.category_group_combo.setCurrentIndex(index)
            
            # メインウィンドウのグループ選択も同期
            parent = self.parentWidget()
            while parent:
                if isinstance(parent, QMainWindow):
                    if hasattr(parent, 'group_combo'):
                        index = parent.group_combo.findText(group_name)
                        if index >= 0:
                            parent.group_combo.setCurrentIndex(index)
                    break
                parent = parent.parentWidget()
            
            self.logger.info(f"グループ選択を同期: {group_name}")
            
        except Exception as e:
            self.logger.exception("グループ選択同期エラー")

    def _on_category_group_changed(self, group_name: str):
        """カテゴリー用グループ選択時のイベント"""
        try:
            self.logger.info(f"選択されたグループ: {group_name}")
            
            # グループ選択の同期
            self._sync_group_selections(group_name)
            
            # 選択されたグループの親カテゴリーを読み込み
            group_id = self._db_manager.get_group_id_by_name(group_name)
            if group_id is not None:
                categories = self._db_manager.get_parent_categories_by_group(group_id)
                self.logger.info(f"グループのカテゴリー: {categories}")
                
                self.parent_list.clear()
                self.parent_list.addItems(categories)
                self.child_list.clear()
            
        except Exception as e:
            self.logger.exception("カテゴリー読み込みエラー")
