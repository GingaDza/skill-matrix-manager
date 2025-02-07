from datetime import datetime

class TimeProvider:
    """時間とユーザー情報の固定プロバイダー"""
    
    # 固定値の設定
    FIXED_TIME = datetime(2025, 2, 7, 12, 11, 26)  # UTC
    FIXED_USER = "GingaDza"

    @staticmethod
    def get_current_time():
        """固定の現在時刻を取得"""
        return TimeProvider.FIXED_TIME

    @staticmethod
    def get_formatted_time():
        """フォーマット済みの時刻文字列を取得"""
        return TimeProvider.FIXED_TIME.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_user():
        """固定のユーザー名を取得"""
        return TimeProvider.FIXED_USER
