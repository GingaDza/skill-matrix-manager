"""表示ユーティリティ"""
from datetime import datetime
import os

def get_timestamp() -> str:
    """現在のタイムスタンプを取得

    Returns:
        str: YYYY-MM-DD HH:MM:SS形式のタイムスタンプ
    """
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def get_username() -> str:
    """現在のユーザー名を取得

    Returns:
        str: 現在のユーザー名
    """
    return os.getenv('USER', os.getenv('USERNAME', 'unknown'))

def display_info():
    """タイムスタンプとユーザー情報を表示"""
    print(f"Current Date and Time (UTC): {get_timestamp()}")
    print(f"Current User's Login: {get_username()}")
