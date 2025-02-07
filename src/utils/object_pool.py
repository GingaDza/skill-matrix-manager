"""オブジェクトプールシステム"""
from typing import Dict, Any, TypeVar, Generic, Optional, Type
import weakref
import logging
from collections import deque

T = TypeVar('T')

class ObjectPool(Generic[T]):
    """
    オブジェクトプールの実装
    
    型安全なオブジェクトの再利用を管理し、
    メモリ使用量を最適化します。
    """
    
    def __init__(self, factory: Type[T], initial_size: int = 10):
        self.logger = logging.getLogger(__name__)
        self._factory = factory
        self._pool: deque[T] = deque(maxlen=100)  # 最大プールサイズ
        self._in_use: Dict[int, weakref.ref] = {}
        
        # 初期プールの作成
        for _ in range(initial_size):
            self._add_to_pool()

    def _add_to_pool(self) -> None:
        """プールに新しいオブジェクトを追加"""
        try:
            obj = self._factory()
            self._pool.append(obj)
        except Exception as e:
            self.logger.error(f"オブジェクト作成エラー: {e}")

    def acquire(self) -> T:
        """プールからオブジェクトを取得"""
        try:
            if not self._pool:
                self._add_to_pool()
            
            obj = self._pool.popleft()
            obj_id = id(obj)
            
            # 使用中オブジェクトの追跡
            self._in_use[obj_id] = weakref.ref(
                obj,
                lambda ref: self._object_collected(obj_id)
            )
            
            return obj
            
        except Exception as e:
            self.logger.error(f"オブジェクト取得エラー: {e}")
            raise

    def release(self, obj: T) -> None:
        """オブジェクトをプールに返却"""
        try:
            obj_id = id(obj)
            if obj_id in self._in_use:
                del self._in_use[obj_id]
                if len(self._pool) < self._pool.maxlen:
                    self._pool.append(obj)
                
        except Exception as e:
            self.logger.error(f"オブジェクト返却エラー: {e}")

    def _object_collected(self, obj_id: int) -> None:
        """オブジェクト回収時のコールバック"""
        try:
            self._in_use.pop(obj_id, None)
        except Exception as e:
            self.logger.error(f"オブジェクト回収エラー: {e}")

    def cleanup(self) -> None:
        """プールのクリーンアップ"""
        try:
            self._in_use.clear()
            self._pool.clear()
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")
