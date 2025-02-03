from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class InputDialog(QDialog):
    def __init__(self, title, label_text, default_text="", parent=None):
        logger.debug(f"Creating InputDialog: title={title}, label={label_text}")
        super().__init__(parent)
        self.current_time = datetime(2025, 2, 3, 10, 39, 38)
        self.current_user = "GingaDza"
        
        try:
            # ダイアログの設定
            self.setWindowTitle(title)
            self.setModal(True)
            logger.debug("Dialog window title and modal set")
            
            # メインレイアウト
            layout = QVBoxLayout(self)
            
            # 入力フィールド
            input_layout = QHBoxLayout()
            self.label = QLabel(label_text)
            self.input_field = QLineEdit()
            self.input_field.setText(default_text)
            input_layout.addWidget(self.label)
            input_layout.addWidget(self.input_field)
            logger.debug("Input field setup complete")
            
            # ボタン
            button_layout = QHBoxLayout()
            ok_button = QPushButton("OK")
            cancel_button = QPushButton("キャンセル")
            
            ok_button.clicked.connect(self.accept)
            cancel_button.clicked.connect(self.reject)
            logger.debug("Buttons connected to slots")
            
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            
            # レイアウトの組み立て
            layout.addLayout(input_layout)
            layout.addLayout(button_layout)
            logger.debug("Dialog layout setup complete")
            
        except Exception as e:
            logger.error(f"Error in InputDialog initialization: {str(e)}")
            logger.exception("Detailed traceback:")
            raise
    
    def get_input(self):
        """入力された値を返す"""
        value = self.input_field.text().strip()
        logger.debug(f"InputDialog returning value: {value}")
        return value