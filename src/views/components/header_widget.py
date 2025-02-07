from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel
)
from PyQt6.QtCore import Qt
from ...utils.time_utils import TimeProvider

class HeaderWidget(QWidget):
    """アプリケーションヘッダーウィジェット"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """UIの設定"""
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 現在時刻（UTC）
        time_label = QLabel(f"Current Date and Time (UTC): {TimeProvider.get_formatted_time()}")
        time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # ユーザー情報
        user_label = QLabel(f"Current User's Login: {TimeProvider.get_current_user()}")
        user_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(time_label)
        layout.addStretch()
        layout.addWidget(user_label)

        # スタイル設定
        self.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 12px;
                padding: 5px;
            }
            QWidget {
                background-color: #f5f5f5;
                border-bottom: 1px solid #dddddd;
            }
        """)
