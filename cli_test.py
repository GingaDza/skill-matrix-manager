#!/usr/bin/env python3
import sqlite3
import logging
import sys
from datetime import datetime

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseCLI:
    def __init__(self):
        self.current_time = "2025-02-07 21:07:26"
        self.db_path = "database/skill_matrix.db"
        self.conn = None
        self.initialize_database()

    def get_connection(self):
        """データベース接続を取得"""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def initialize_database(self):
        """データベースの初期化"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # グループテーブル
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        ''')

        # ユーザーテーブル
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_id INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            deleted_at TEXT DEFAULT NULL,
            FOREIGN KEY (group_id) REFERENCES groups (id)
        )
        ''')

        # 初期データの確認と挿入
        cursor.execute("SELECT COUNT(*) FROM groups")
        if cursor.fetchone()[0] == 0:
            groups = [
                ("開発部", self.current_time, self.current_time),
                ("営業部", self.current_time, self.current_time),
                ("管理部", self.current_time, self.current_time)
            ]
            cursor.executemany(
                "INSERT INTO groups (name, created_at, updated_at) VALUES (?, ?, ?)",
                groups
            )
        
        conn.commit()
        logger.info("Database initialized successfully")

    def list_groups(self):
        """グループ一覧を表示"""
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, name FROM groups ORDER BY id")
        groups = cursor.fetchall()
        
        print("\n=== グループ一覧 ===")
        for group_id, name in groups:
            print(f"ID: {group_id}, 名前: {name}")
        return groups

    def list_users(self, group_id):
        """ユーザー一覧を表示"""
        cursor = self.get_connection().cursor()
        cursor.execute("""
            SELECT u.id, u.name, g.name 
            FROM users u 
            JOIN groups g ON u.group_id = g.id 
            WHERE u.group_id = ? AND u.deleted_at IS NULL
            ORDER BY u.id
        """, (group_id,))
        users = cursor.fetchall()
        
        print(f"\n=== ユーザー一覧 (グループID: {group_id}) ===")
        for user_id, name, group_name in users:
            print(f"ID: {user_id}, 名前: {name}, グループ: {group_name}")
        return users

    def add_user(self, name, group_id):
        """ユーザーを追加"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # グループの存在確認
            cursor.execute("SELECT id FROM groups WHERE id = ?", (group_id,))
            if not cursor.fetchone():
                print(f"エラー: グループID {group_id} が存在しません")
                return False
            
            # ユーザーの追加
            cursor.execute("""
                INSERT INTO users (name, group_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (name, group_id, self.current_time, self.current_time))
            
            conn.commit()
            print(f"ユーザー '{name}' を追加しました (ID: {cursor.lastrowid})")
            return True
            
        except sqlite3.Error as e:
            print(f"データベースエラー: {e}")
            conn.rollback()
            return False

    def edit_user(self, user_id, new_name):
        """ユーザーを編集"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users 
                SET name = ?, updated_at = ? 
                WHERE id = ? AND deleted_at IS NULL
            """, (new_name, self.current_time, user_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"ユーザーID {user_id} の名前を '{new_name}' に変更しました")
                return True
            else:
                print(f"エラー: ユーザーID {user_id} が見つかりません")
                return False
                
        except sqlite3.Error as e:
            print(f"データベースエラー: {e}")
            conn.rollback()
            return False

    def delete_user(self, user_id):
        """ユーザーを削除"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users 
                SET deleted_at = ?, updated_at = ? 
                WHERE id = ? AND deleted_at IS NULL
            """, (self.current_time, self.current_time, user_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"ユーザーID {user_id} を削除しました")
                return True
            else:
                print(f"エラー: ユーザーID {user_id} が見つかりません")
                return False
                
        except sqlite3.Error as e:
            print(f"データベースエラー: {e}")
            conn.rollback()
            return False

    def close(self):
        """データベース接続を閉じる"""
        if self.conn:
            self.conn.close()
            self.conn = None

def main():
    cli = DatabaseCLI()
    
    while True:
        print("\n=== スキルマトリックス管理システム CLI ===")
        print("1: グループ一覧表示")
        print("2: ユーザー一覧表示")
        print("3: ユーザー追加")
        print("4: ユーザー編集")
        print("5: ユーザー削除")
        print("0: 終了")
        
        try:
            choice = input("\n選択してください: ")
            
            if choice == "0":
                break
            elif choice == "1":
                cli.list_groups()
            elif choice == "2":
                group_id = int(input("グループIDを入力してください: "))
                cli.list_users(group_id)
            elif choice == "3":
                name = input("ユーザー名を入力してください: ")
                group_id = int(input("グループIDを入力してください: "))
                cli.add_user(name, group_id)
            elif choice == "4":
                user_id = int(input("編集するユーザーIDを入力してください: "))
                new_name = input("新しいユーザー名を入力してください: ")
                cli.edit_user(user_id, new_name)
            elif choice == "5":
                user_id = int(input("削除するユーザーIDを入力してください: "))
                cli.delete_user(user_id)
            else:
                print("無効な選択です")
                
        except ValueError as e:
            print("入力エラー: 正しい値を入力してください")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    
    cli.close()
    print("プログラムを終了します")

if __name__ == "__main__":
    main()
