"""データ管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox,
    QTabWidget
)
from ...database.database_manager import DatabaseManager
import logging

class DataManagementWidget(QWidget):
    """データ管理ウィジェットクラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タブウィジェット
        tab_widget = QTabWidget()
        
        # データインポートタブ
        import_tab = QWidget()
        import_layout = QVBoxLayout(import_tab)
        
        import_group_btn = QPushButton("グループデータをインポート")
        import_group_btn.clicked.connect(self._import_group_data)
        import_layout.addWidget(import_group_btn)
        
        import_category_btn = QPushButton("カテゴリーデータをインポート")
        import_category_btn.clicked.connect(self._import_category_data)
        import_layout.addWidget(import_category_btn)
        
        import_skill_btn = QPushButton("スキルデータをインポート")
        import_skill_btn.clicked.connect(self._import_skill_data)
        import_layout.addWidget(import_skill_btn)
        
        tab_widget.addTab(import_tab, "データインポート")
        
        # データエクスポートタブ
        export_tab = QWidget()
        export_layout = QVBoxLayout(export_tab)
        
        export_data_btn = QPushButton("データをエクスポート")
        export_data_btn.clicked.connect(self._export_data)
        export_layout.addWidget(export_data_btn)
        
        export_chart_btn = QPushButton("レーダーチャートをエクスポート")
        export_chart_btn.clicked.connect(self._export_chart)
        export_layout.addWidget(export_chart_btn)
        
        tab_widget.addTab(export_tab, "データエクスポート")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)

    def _import_group_data(self):
        """グループデータをインポートする"""
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "グループデータを選択",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            try:
                self._db_manager.import_group_data(filename)
                QMessageBox.information(
                    self,
                    "成功",
                    "グループデータをインポートしました"
                )
            except Exception as e:
                self.logger.exception("グループデータのインポートに失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループデータのインポートに失敗しました: {str(e)}"
                )

    def _import_category_data(self):
        """カテゴリーデータをインポートする"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "カテゴリーデータを選択",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            try:
                self._db_manager.import_category_data(filename)
                QMessageBox.information(
                    self,
                    "成功",
                    "カテゴリーデータをインポートしました"
                )
            except Exception as e:
                self.logger.exception("カテゴリーデータのインポートに失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーデータのインポートに失敗しました: {str(e)}"
                )

    def _import_skill_data(self):
        """スキルデータをインポートする"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "スキルデータを選択",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            try:
                self._db_manager.import_skill_data(filename)
                QMessageBox.information(
                    self,
                    "成功",
                    "スキルデータをインポートしました"
                )
            except Exception as e:
                self.logger.exception("スキルデータのインポートに失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"スキルデータのインポートに失敗しました: {str(e)}"
                )

    def _export_data(self):
        """データをエクスポートする"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "データを保存",
            "",
            "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            try:
                self._db_manager.export_data(filename)
                QMessageBox.information(
                    self,
                    "成功",
                    "データをエクスポートしました"
                )
            except Exception as e:
                self.logger.exception("データのエクスポートに失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"データのエクスポートに失敗しました: {str(e)}"
                )

    def _export_chart(self):
        """レーダーチャートをエクスポートする"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "レーダーチャートを保存",
            "",
            "PDF Files (*.pdf);;PNG Files (*.png);;All Files (*)"
        )
        if filename:
            try:
                self._db_manager.export_chart(filename)
                QMessageBox.information(
                    self,
                    "成功",
                    "レーダーチャートをエクスポートしました"
                )
            except Exception as e:
                self.logger.exception("レーダーチャートのエクスポートに失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"レーダーチャートのエクスポートに失敗しました: {str(e)}"
                )
