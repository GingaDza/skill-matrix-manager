# src/app/utils/db.py
"""
このモジュールは廃止予定です。
データベース関連の機能は src.app.database と src.app.utils.deps に移動しました。
"""
from ..utils.deps import get_db

__all__ = ['get_db']