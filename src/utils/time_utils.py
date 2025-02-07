from datetime import datetime

class TimeProvider:
    """時間とユーザー情報の固定プロバイダー"""
    
    # 固定値の設定
    FIXED_TIME = datetime(2025, 2, 7, 12, 13, 1)  # UTC
    _current_user = "GingaDza"  # デフォルトユーザー

    @classmethod
    def set_current_user(cls, username):
        """現在のユーザーを設定"""
        cls._current_user = username

    @classmethod
    def get_current_user(cls):
        """現在のユーザーを取得"""
        return cls._current_user

    @classmethod
    def get_current_time(cls):
        """固定の現在時刻を取得"""
        return cls.FIXED_TIME

    @classmethod
    def get_formatted_time(cls):
        """フォーマット済みの時刻文字列を取得"""
        return cls.FIXED_TIME.strftime("%Y-%m-%d %H:%M:%S")
