from PyQt6.QtWidgets import QApplication
from .views.main_window import MainWindow

class App(QApplication):
    def __init__(self):
        super().__init__([])
        self.main_window = MainWindow()
        self.main_window.show()

    def exec(self):
        """アプリケーションの実行"""
        return super().exec()
