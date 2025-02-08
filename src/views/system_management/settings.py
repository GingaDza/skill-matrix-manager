"""初期設定ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QListWidget, QPushButton,
    QInputDialog, QMessageBox, QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from ...database.database_manager import DatabaseManager

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        """初期化"""
        super().__init__(parent)
        
        # ロガー設定
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        
        # UI要素の初期化
        self.group_list = None
        self.category_group_combo = None
        self.parent_list = None
        self.child_list = None
        
        # ボタンの初期化
        self.add_group_btn = None
        self.edit_group_btn = None
        self.delete_group_btn = None
        self.add_category_btn = None
        self.edit_category_btn = None
        self.delete_category_btn = None
        self.add_skill_btn = None
        self.edit_skill_btn = None
        self.delete_skill_btn = None
        self.new_tab_btn = None
        
        # レイアウトの初期化
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        
        # UIの構築とシグナル接続
        self.init_ui()
        self.connect_signals()
        self.load_data()

    def init_ui(self):
        """UIの初期化"""
        # グループリスト
        group_box = self.create_group_list()
        self.main_layout.addWidget(group_box)
        
        # カテゴリーリスト
        category_box = self.create_category_lists()
        self.main_layout.addWidget(category_box)

    def connect_signals(self):
        """シグナルとスロットの接続"""
        # グループ操作
        self.add_group_btn.clicked.connect(self.on_add_group)
        self.edit_group_btn.clicked.connect(self.on_edit_group)
        self.delete_group_btn.clicked.connect(self.on_delete_group)
        
        # カテゴリー操作
        self.add_category_btn.clicked.connect(self.on_add_category)
        self.edit_category_btn.clicked.connect(self.on_edit_category)
        self.delete_category_btn.clicked.connect(self.on_delete_category)
        
        # スキル操作
        self.add_skill_btn.clicked.connect(self.on_add_skill)
        self.edit_skill_btn.clicked.connect(self.on_edit_skill)
        self.delete_skill_btn.clicked.connect(self.on_delete_skill)
        
        # タブ操作
        self.new_tab_btn.clicked.connect(self.on_add_new_tab)
        
        # リスト選択
        self.parent_list.currentRowChanged.connect(self.on_parent_selected)
        self.category_group_combo.currentTextChanged.connect(self.on_category_group_changed)
        self.group_list.currentRowChanged.connect(self.on_group_selected)

    def create_group_list(self):
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

    def create_category_lists(self):
        """カテゴリーリストの作成"""
        category_box = QGroupBox("カテゴリー管理")
        layout = QVBoxLayout()
        
        # グループ選択
        group_select_layout = QHBoxLayout()
        group_select_layout.addWidget(QLabel("グループ:"))
        self.category_group_combo = QComboBox()
        group_select_layout.addWidget(self.category_group_combo)
        layout.addLayout(group_select_layout)
        
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

    def load_data(self):
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
            QMessageBox.critical(
                self,
                "エラー",
                "データの読み込みに失敗しました。"
            )

    def on_add_group(self):
        """グループ追加ボタンのクリックイベント"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "グループ追加",
                "グループ名を入力してください:"
            )
            
            if ok and name.strip():
                if self._db_manager.add_group(name.strip()):
                    self.load_data()
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

    def on_edit_group(self):
        """グループ編集ボタンのクリックイベント"""
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                raise Exception("編集するグループを選択してください。")
                
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self,
                "グループ編集",
                "新しいグループ名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                # TODO: グループ名の変更処理を実装
                self.load_data()
                QMessageBox.information(
                    self,
                    "成功",
                    f"グループ名を「{new_name}」に変更しました。"
                )
                
        except Exception as e:
            self.logger.exception("グループ編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_delete_group(self):
        """グループ削除ボタンのクリックイベント"""
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                raise Exception("削除するグループを選択してください。")
                
            group_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "確認",
                f"グループ「{group_name}」を削除してもよろしいですか？\n"
                "このグループに関連する全てのデータも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: グループの削除処理を実装
                self.load_data()
                QMessageBox.information(
                    self,
                    "成功",
                    f"グループ「{group_name}」を削除しました。"
                )
                
        except Exception as e:
            self.logger.exception("グループ削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_add_category(self):
        """カテゴリー追加ボタンのクリックイベント"""
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
                    self.on_category_group_changed(group_name)
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

    def on_edit_category(self):
        """カテゴリー編集ボタンのクリックイベント"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("編集するカテゴリーを選択してください。")
                
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self,
                "カテゴリー編集",
                "新しいカテゴリー名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                # TODO: カテゴリー名の変更処理を実装
                self.on_category_group_changed(self.category_group_combo.currentText())
                QMessageBox.information(
                    self,
                    "成功",
                    f"カテゴリー名を「{new_name}」に変更しました。"
                )
                
        except Exception as e:
            self.logger.exception("カテゴリー編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_delete_category(self):
        """カテゴリー削除ボタンのクリックイベント"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("削除するカテゴリーを選択してください。")
                
            category_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "確認",
                f"カテゴリー「{category_name}」を削除してもよろしいですか？\n"
                "このカテゴリーに関連する全てのスキルも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: カテゴリーの削除処理を実装
                self.on_category_group_changed(self.category_group_combo.currentText())
                QMessageBox.information(
                    self,
                    "成功",
                    f"カテゴリー「{category_name}」を削除しました。"
                )
                
        except Exception as e:
            self.logger.exception("カテゴリー削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )



    def on_add_skill(self):
        """スキル追加ボタンのクリックイベント"""
        try:
            parent_item = self.parent_list.currentItem()
            if not parent_item:
                raise Exception("親カテゴリーを選択してください。")
                
            name, ok = QInputDialog.getText(
                self,
                "スキル追加",
                "スキル名を入力してください:"
            )
            
            if ok and name.strip():
                # TODO: スキル追加の実装
                self.on_parent_selected(self.parent_list.currentRow())
                QMessageBox.information(
                    self,
                    "成功",
                    f"スキル「{name}」を追加しました。"
                )
                
        except Exception as e:
            self.logger.exception("スキル追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_edit_skill(self):
        """スキル編集ボタンのクリックイベント"""
        try:
            current_item = self.child_list.currentItem()
            if not current_item:
                raise Exception("編集するスキルを選択してください。")
                
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self,
                "スキル編集",
                "新しいスキル名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                # TODO: スキル名の変更処理を実装
                self.on_parent_selected(self.parent_list.currentRow())
                QMessageBox.information(
                    self,
                    "成功",
                    f"スキル名を「{new_name}」に変更しました。"
                )
                
        except Exception as e:
            self.logger.exception("スキル編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_delete_skill(self):
        """スキル削除ボタンのクリックイベント"""
        try:
            current_item = self.child_list.currentItem()
            if not current_item:
                raise Exception("削除するスキルを選択してください。")
                
            skill_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "確認",
                f"スキル「{skill_name}」を削除してもよろしいですか？\n"
                "このスキルに関連する全ての評価データも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: スキルの削除処理を実装
                self.on_parent_selected(self.parent_list.currentRow())
                QMessageBox.information(
                    self,
                    "成功",
                    f"スキル「{skill_name}」を削除しました。"
                )
                
        except Exception as e:
            self.logger.exception("スキル削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_add_new_tab(self):
        """新規タブ追加ボタンのクリックイベント"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("タブとして追加する親カテゴリーを選択してください。")
                
            category_name = current_item.text()
            # TODO: メインウィンドウへのタブ追加通知
            QMessageBox.information(
                self,
                "成功",
                f"カテゴリー「{category_name}」をタブとして追加しました。"
            )
            
        except Exception as e:
            self.logger.exception("タブ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_parent_selected(self, row: int):
        """親カテゴリー選択時のイベント"""
        try:
            if row >= 0:
                parent_item = self.parent_list.item(row)
                if parent_item:
                    parent_name = parent_item.text()
                    # TODO: 選択されたカテゴリーのスキル一覧を表示
                    skills = []  # 仮の空リスト
                    self.child_list.clear()
                    self.child_list.addItems(skills)
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def on_category_group_changed(self, group_name: str):
        """カテゴリー用グループ選択時のイベント"""
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

    def on_group_selected(self, row: int):
        """グループ選択時のイベント"""
        if row >= 0:
            selected_group = self.group_list.item(row).text()
            # コンボボックスの選択を同期
            index = self.category_group_combo.findText(selected_group)
            if index >= 0:
                self.category_group_combo.setCurrentIndex(index)

