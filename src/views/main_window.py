"""メインウィンドウモジュール"""
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QComboBox, QSpinBox,
    QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from ..database.database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("メインウィンドウを初期化中...")
        
        self._db_manager = db_manager
        self._init_ui()
        self._load_data()

    def _init_ui(self):
        """UIの初期化"""
        try:
            # ウィンドウの基本設定
            self.setWindowTitle("スキルマトリックス管理")
            self.setMinimumSize(1200, 800)
            
            # セントラルウィジェット
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # メインレイアウト
            main_layout = QVBoxLayout()
            central_widget.setLayout(main_layout)
            
            # タブウィジェット
            self.tab_widget = QTabWidget()
            main_layout.addWidget(self.tab_widget)
            
            # スキルタブの追加
            self._add_skills_tab()
            
            # カテゴリタブの追加
            self._add_categories_tab()
            
            # ステータスバー
            self.statusBar().showMessage("準備完了")
            
            self.logger.info("メインウィンドウのUI初期化完了")
            
        except Exception as e:
            self.logger.exception("UIコンポーネントの初期化エラー")
            raise

    def _add_skills_tab(self):
        """スキルタブの追加"""
        skills_tab = QWidget()
        layout = QVBoxLayout()
        skills_tab.setLayout(layout)
        
        # コントロールエリア
        controls = QHBoxLayout()
        
        # カテゴリ選択
        self.category_combo = QComboBox()
        self.category_combo.addItem("全て")
        controls.addWidget(QLabel("カテゴリ:"))
        controls.addWidget(self.category_combo)
        
        # レベル選択
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 5)
        controls.addWidget(QLabel("レベル:"))
        controls.addWidget(self.level_spin)
        
        # 検索
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("検索...")
        controls.addWidget(self.search_input)
        
        # ボタン
        add_btn = QPushButton("追加")
        add_btn.clicked.connect(self._add_skill)
        controls.addWidget(add_btn)
        
        layout.addLayout(controls)
        
        # スキルテーブル
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(4)
        self.skills_table.setHorizontalHeaderLabels([
            "スキル名", "カテゴリ", "レベル", "最終更新"
        ])
        self.skills_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.skills_table)
        
        self.tab_widget.addTab(skills_tab, "スキル一覧")

    def _add_categories_tab(self):
        """カテゴリタブの追加"""
        categories_tab = QWidget()
        layout = QVBoxLayout()
        categories_tab.setLayout(layout)
        
        # コントロールエリア
        controls = QHBoxLayout()
        
        # カテゴリ名入力
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("新しいカテゴリ名...")
        controls.addWidget(self.category_input)
        
        # 追加ボタン
        add_btn = QPushButton("カテゴリ追加")
        add_btn.clicked.connect(self._add_category)
        controls.addWidget(add_btn)
        
        layout.addLayout(controls)
        
        # カテゴリテーブル
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(3)
        self.categories_table.setHorizontalHeaderLabels([
            "カテゴリ名", "スキル数", "最終更新"
        ])
        self.categories_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.categories_table)
        
        self.tab_widget.addTab(categories_tab, "カテゴリ管理")

    @pyqtSlot()
    def _add_skill(self):
        """スキルの追加"""
        try:
            skill_name = self.search_input.text().strip()
            category = self.category_combo.currentText()
            level = self.level_spin.value()
            
            if not skill_name:
                QMessageBox.warning(
                    self,
                    "入力エラー",
                    "スキル名を入力してください。"
                )
                return
                
            # TODO: データベースに追加
            self._load_skills_data()
            self.search_input.clear()
            self.statusBar().showMessage("スキルを追加しました")
            
        except Exception as e:
            self.logger.exception("スキル追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                "スキルの追加に失敗しました。"
            )

    @pyqtSlot()
    def _add_category(self):
        """カテゴリの追加"""
        try:
            category_name = self.category_input.text().strip()
            
            if not category_name:
                QMessageBox.warning(
                    self,
                    "入力エラー",
                    "カテゴリ名を入力してください。"
                )
                return
                
            # TODO: データベースに追加
            self._load_categories_data()
            self.category_input.clear()
            self.statusBar().showMessage("カテゴリを追加しました")
            
        except Exception as e:
            self.logger.exception("カテゴリ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                "カテゴリの追加に失敗しました。"
            )

    def _load_data(self):
        """データの読み込み"""
        try:
            self._load_categories_data()
            self._load_skills_data()
            
        except Exception as e:
            self.logger.exception("データ読み込みエラー")
            QMessageBox.critical(
                self,
                "エラー",
                "データの読み込みに失敗しました。"
            )

    def _load_categories_data(self):
        """カテゴリデータの読み込み"""
        try:
            # TODO: データベースからカテゴリを読み込み
            self.categories_table.setRowCount(0)
            self.category_combo.clear()
            self.category_combo.addItem("全て")
            
        except Exception as e:
            self.logger.exception("カテゴリデータ読み込みエラー")
            raise

    def _load_skills_data(self):
        """スキルデータの読み込み"""
        try:
            # TODO: データベースからスキルを読み込み
            self.skills_table.setRowCount(0)
            
        except Exception as e:
            self.logger.exception("スキルデータ読み込みエラー")
            raise

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        try:
            self._cleanup()
            event.accept()
            
        except Exception as e:
            self.logger.exception("終了処理エラー")
            event.ignore()

    def _cleanup(self):
        """リソースのクリーンアップ"""
        try:
            self._db_manager = None
            self.logger.info("メインウィンドウのクリーンアップ完了")
            
        except Exception as e:
            self.logger.exception("クリーンアップエラー")
            raise
