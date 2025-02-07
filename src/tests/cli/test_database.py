import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DatabaseTest:
    def __init__(self):
        self.db = DatabaseManager("test.db")

    def test_user_operations(self):
        """ユーザー関連の操作をテスト"""
        try:
            # グループの作成
            group_id = self.db.add_group("テスト開発チーム", "テスト用グループ")
            print(f"Created group with ID: {group_id}")

            # ユーザーの追加
            user_id = self.db.add_user("testuser1", group_id)
            print(f"Added user with ID: {user_id}")

            # ユーザー情報の取得
            user = self.db.get_user(user_id)
            print(f"Retrieved user: {user}")

            # ユーザーリストの取得
            users = self.db.get_users_by_group(group_id)
            print(f"Users in group: {users}")

            # ユーザー情報の更新
            self.db.update_user(user_id, "updated_user", group_id)
            updated_user = self.db.get_user(user_id)
            print(f"Updated user: {updated_user}")

            # ユーザーの削除
            self.db.delete_user(user_id)
            remaining_users = self.db.get_users_by_group(group_id)
            print(f"Remaining users: {remaining_users}")

            return True

        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            return False

def main():
    test = DatabaseTest()
    success = test.test_user_operations()
    print(f"Test {'succeeded' if success else 'failed'}")

if __name__ == "__main__":
    main()
