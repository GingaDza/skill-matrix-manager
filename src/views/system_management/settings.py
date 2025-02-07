"""初期設定ウィジェット"""
# [以前の import 文は保持...]

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()
        self._connect_signals()
        self._load_data()

    # [_init_ui と _create_group_list メソッドは保持...]

    def _create_category_lists(self):
        """カテゴリーリストの作成"""
        category_box = QGroupBox("カテゴリー管理")
        layout = QVBoxLayout()
        
        # グループ選択
        group_select_layout = QHBoxLayout()
        group_select_layout.addWidget(QLabel("グループ:"))
        self.category_group_combo = QComboBox()
        self.category_group_combo.currentTextChanged.connect(self._on_category_group_changed)
        group_select_layout.addWidget(self.category_group_combo)
        layout.addLayout(group_select_layout)
        
        # [以前のカテゴリーリストのUIは保持...]
        
        return category_box

    def _connect_signals(self):
        """シグナルの接続"""
        # グループ操作
        self.add_group_btn.clicked.connect(self._add_group)
        self.edit_group_btn.clicked.connect(self._edit_group)
        self.delete_group_btn.clicked.connect(self._delete_group)
        self.group_list.currentRowChanged.connect(self._on_group_selected)
        
        # [他のシグナル接続は保持...]

    def _load_data(self):
        """データの読み込み"""
        try:
            # グループの読み込み
            groups = self._db_manager.get_groups()
            
            # グループリストの更新
            self.group_list.clear()
            self.group_list.addItems(groups)
            
            # グループコンボボックスの更新
            self.category_group_combo.clear()
            self.category_group_combo.addItems(groups)
            
        except Exception as e:
            self.logger.exception("データ読み込みエラー")
            QMessageBox.critical(self, "エラー", "データの読み込みに失敗しました。")

    def _add_group(self):
        """グループの追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "グループ追加",
                "グループ名を入力してください:"
            )
            
            if ok and name.strip():
                if self._db_manager.add_group(name.strip()):
                    self._load_data()  # 両方のリストを更新
                    QMessageBox.information(
                        self,
                        "成功",
                        f"グループ「{name}」を追加しました。"
                    )
                else:
                    raise Exception("グループの追加に失敗しました。")
                    
        except Exception as e:
            self.logger.exception("グループ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_group_selected(self, row: int):
        """グループ選択時の処理"""
        if row >= 0:
            selected_group = self.group_list.item(row).text()
            # コンボボックスの選択を同期
            index = self.category_group_combo.findText(selected_group)
            if index >= 0:
                self.category_group_combo.setCurrentIndex(index)

    def _on_category_group_changed(self, group_name: str):
        """カテゴリー用グループ選択時の処理"""
        try:
            # グループリストの選択を同期
            items = self.group_list.findItems(group_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.group_list.setCurrentItem(items[0])
            
            # 選択されたグループの親カテゴリーを読み込み
            group_id = self._db_manager.get_group_id_by_name(group_name)
            if group_id is not None:
                categories = self._db_manager.get_parent_categories_by_group(group_id)
                self.parent_list.clear()
                self.parent_list.addItems(categories)
                self.child_list.clear()
            
        except Exception as e:
            self.logger.exception("カテゴリー読み込みエラー")

    def _add_category(self):
        """カテゴリーの追加"""
        try:
            group_name = self.category_group_combo.currentText()
            if not group_name:
                raise Exception("グループを選択してください。")
            
            name, ok = QInputDialog.getText(
                self,
                "カテゴリー追加",
                "カテゴリー名を入力してください:"
            )
            
            if ok and name.strip():
                group_id = self._db_manager.get_group_id_by_name(group_name)
                if group_id is None:
                    raise Exception("グループが見つかりません。")
                
                if self._db_manager.add_parent_category(name.strip(), group_id):
                    self._on_category_group_changed(group_name)  # カテゴリーリストを更新
                    QMessageBox.information(
                        self,
                        "成功",
                        f"カテゴリー「{name}」を追加しました。"
                    )
                else:
                    raise Exception("カテゴリーの追加に失敗しました。")
                    
        except Exception as e:
            self.logger.exception("カテゴリー追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    # [その他のメソッドは保持...]

