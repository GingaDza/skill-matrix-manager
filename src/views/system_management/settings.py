"""初期設定ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QListWidget, QPushButton,
    QInputDialog, QMessageBox
)
from ...database.database_manager import DatabaseManager

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()
        self._connect_signals()
        self._load_data()

    def _init_ui(self):
        """UIの初期化"""
        layout = QHBoxLayout()
        
        # グループリスト
        group_box = self._create_group_list()
        layout.addWidget(group_box)
        
        # カテゴリーリスト
        category_box = self._create_category_lists()
        layout.addWidget(category_box)
        
        self.setLayout(layout)

    def _create_group_list(self):
        """グループリストの作成"""
        group_box = QGroupBox("グループリスト")
        layout = QVBoxLayout()
        
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        button_layout.addWidget(self.add_group_btn)
        button_layout.addWidget(self.edit_group_btn)
        button_layout.addWidget(self.delete_group_btn)
        
        layout.addLayout(button_layout)
        group_box.setLayout(layout)
        return group_box

    def _create_category_lists(self):
        """カテゴリーリストの作成"""
        category_box = QGroupBox("カテゴリー管理")
        layout = QVBoxLayout()
        
        # 親カテゴリー
        parent_box = QGroupBox("親カテゴリー")
        parent_layout = QVBoxLayout()
        self.parent_list = QListWidget()
        parent_layout.addWidget(self.parent_list)
        parent_box.setLayout(parent_layout)
        
        # 子カテゴリー
        child_box = QGroupBox("子カテゴリー")
        child_layout = QVBoxLayout()
        self.child_list = QListWidget()
        child_layout.addWidget(self.child_list)
        child_box.setLayout(child_layout)
        
        layout.addWidget(parent_box)
        layout.addWidget(child_box)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        self.add_category_btn = QPushButton("カテゴリー追加")
        self.edit_category_btn = QPushButton("カテゴリー編集")
        self.delete_category_btn = QPushButton("カテゴリー削除")
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_skill_btn = QPushButton("スキル編集")
        self.delete_skill_btn = QPushButton("スキル削除")
        self.new_tab_btn = QPushButton("新規タブ追加")
        
        button_layout.addWidget(self.add_category_btn)
        button_layout.addWidget(self.edit_category_btn)
        button_layout.addWidget(self.delete_category_btn)
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_skill_btn)
        button_layout.addWidget(self.delete_skill_btn)
        button_layout.addWidget(self.new_tab_btn)
        
        layout.addLayout(button_layout)
        category_box.setLayout(layout)
        return category_box

    def _connect_signals(self):
        """シグナルの接続"""
        # グループ操作
        self.add_group_btn.clicked.connect(self._add_group)
        self.edit_group_btn.clicked.connect(self._edit_group)
        self.delete_group_btn.clicked.connect(self._delete_group)
        
        # カテゴリー操作
        self.add_category_btn.clicked.connect(self._add_category)
        self.edit_category_btn.clicked.connect(self._edit_category)
        self.delete_category_btn.clicked.connect(self._delete_category)
        
        # スキル操作
        self.add_skill_btn.clicked.connect(self._add_skill)
        self.edit_skill_btn.clicked.connect(self._edit_skill)
        self.delete_skill_btn.clicked.connect(self._delete_skill)
        
        # タブ操作
        self.new_tab_btn.clicked.connect(self._add_new_tab)
        
        # リスト選択
        self.parent_list.currentRowChanged.connect(self._on_parent_selected)

    def _load_data(self):
        """データの読み込み"""
        try:
            # グループの読み込み
            groups = self._db_manager.get_groups()
            self.group_list.clear()
            self.group_list.addItems(groups)
            
            # 親カテゴリーの読み込み
            categories = self._db_manager.get_parent_categories()
            self.parent_list.clear()
            self.parent_list.addItems(categories)
            
        except Exception as e:
            self.logger.exception("データ読み込みエラー")
            QMessageBox.critical(
                self,
                "エラー",
                "データの読み込みに失敗しました。"
            )

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
                    self._load_data()
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

    def _edit_group(self):
        """グループの編集"""
        # TODO: 実装
        pass

    def _delete_group(self):
        """グループの削除"""
        # TODO: 実装
        pass

    def _add_category(self):
        """カテゴリーの追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "カテゴリー追加",
                "カテゴリー名を入力してください:"
            )
            
            if ok and name.strip():
                if self._db_manager.add_parent_category(name.strip()):
                    self._load_data()
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

    def _edit_category(self):
        """カテゴリーの編集"""
        # TODO: 実装
        pass

    def _delete_category(self):
        """カテゴリーの削除"""
        # TODO: 実装
        pass

    def _add_skill(self):
        """スキルの追加"""
        try:
            current_parent = self.parent_list.currentItem()
            if not current_parent:
                raise Exception("親カテゴリーを選択してください。")
                
            name, ok = QInputDialog.getText(
                self,
                "スキル追加",
                "スキル名を入力してください:"
            )
            
            if ok and name.strip():
                # TODO: 親カテゴリーIDの取得処理
                parent_id = 1  # 仮のID
                
                if self._db_manager.add_skill(name.strip(), parent_id):
                    self._on_parent_selected(self.parent_list.currentRow())
                    QMessageBox.information(
                        self,
                        "成功",
                        f"スキル「{name}」を追加しました。"
                    )
                else:
                    raise Exception("スキルの追加に失敗しました。")
                    
        except Exception as e:
            self.logger.exception("スキル追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _edit_skill(self):
        """スキルの編集"""
        # TODO: 実装
        pass

    def _delete_skill(self):
        """スキルの削除"""
        # TODO: 実装
        pass

    def _add_new_tab(self):
        """新規タブの追加"""
        try:
            current_parent = self.parent_list.currentItem()
            if not current_parent:
                raise Exception("親カテゴリーを選択してください。")
                
            # メインウィンドウにタブ追加を通知
            # TODO: シグナル実装
            pass
            
        except Exception as e:
            self.logger.exception("タブ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_parent_selected(self, row: int):
        """親カテゴリー選択時の処理"""
        try:
            if row >= 0:
                parent_name = self.parent_list.item(row).text()
                skills = self._db_manager.get_skills_by_parent(parent_name)
                
                self.child_list.clear()
                self.child_list.addItems(skills)
                
        except Exception as e:
            self.logger.exception("スキル一覧取得エラー")
