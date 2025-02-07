from datetime import datetime

class TimeProvider:
    """時間とユーザー情報の管理クラス"""
    
    _current_user = None

    @staticmethod
    def get_current_time():
        """現在時刻を取得"""
        return datetime.utcnow()

    @staticmethod
    def get_current_user():
        """現在のユーザーを取得"""
        return TimeProvider._current_user or "GingaDza"

    @staticmethod
    def set_current_user(username):
        """現在のユーザーを設定"""
        TimeProvider._current_user = username
