from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt
import sys
import platform
import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemInfoTab(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime.now()
        self.current_user = "GingaDza"
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # システム情報表示用のテキストエディット
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        layout.addWidget(self.info_display)
        
        # システム情報の更新
        self.update_system_info()

    def update_system_info(self):
        try:
            info = []
            
            # 基本システム情報
            info.append("=== System Information ===")
            info.append(f"Current Time (UTC): {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            info.append(f"Current User: {self.current_user}")
            info.append(f"Python Version: {sys.version.split()[0]}")
            info.append(f"Platform: {platform.platform()}")
            info.append(f"SQLite Version: {sqlite3.sqlite_version}")
            
            # データベース情報
            info.append("\n=== Database Statistics ===")
            try:
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                # テーブル統計
                tables = ['departments', 'users', 'skill_categories', 'user_skills']
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    info.append(f"{table}: {count} records")
                
                # グループ統計
                cursor.execute("""
                    SELECT d.name, COUNT(u.id) as user_count
                    FROM departments d
                    LEFT JOIN users u ON d.id = u.department_id
                    GROUP BY d.name
                    ORDER BY user_count DESC
                """)
                info.append("\n=== Group Statistics ===")
                for group in cursor.fetchall():
                    info.append(f"{group[0]}: {group[1]} users")
                
                # スキル統計
                cursor.execute("""
                    SELECT sc.name, COUNT(us.user_id) as user_count, 
                           AVG(us.level) as avg_level
                    FROM skill_categories sc
                    LEFT JOIN user_skills us ON sc.id = us.skill_id
                    WHERE sc.parent_id IS NOT NULL
                    GROUP BY sc.name
                    ORDER BY user_count DESC
                """)
                info.append("\n=== Skill Statistics ===")
                for skill in cursor.fetchall():
                    avg_level = skill[2] if skill[2] is not None else 0
                    info.append(f"{skill[0]}: {skill[1]} users (Avg. Level: {avg_level:.1f})")
                
            except Exception as db_error:
                logger.error(f"Database statistics error: {db_error}")
                info.append("\nError retrieving database statistics")
            
            # 情報の表示
            self.info_display.setPlainText("\n".join(info))
            
        except Exception as e:
            logger.error(f"Error updating system info: {e}")
            self.info_display.setPlainText("Error loading system information")
