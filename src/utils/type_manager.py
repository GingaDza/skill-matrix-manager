"""型管理システム"""
from typing import Dict, Any, Type, TypeVar, Optional
import weakref
import logging
import gc
from .object_pool import ObjectPool

T = TypeVar('T')

class TypeManager:
    """
    型システムの管理クラス
    
    型のキャッシュと再利用を管理し、
    メモリリークを防ぎます。
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """初期化"""
        self.logger = logging.getLogger(__name__)
        self._type_cache: Dict[str, weakref.ref] = {}
        self._dict_pool = ObjectPool(dict, initial_size=50)
        self._tuple_pool = ObjectPool(tuple, initial_size=50)

    def get_cached_type(self, type_key: str) -> Optional[Type]:
        """型キャッシュからの取得"""
        try:
            ref = self._type_cache.get(type_key)
            if ref is not None:
                cached_type = ref()
                if cached_type is not None:
                    return cached_type
                self._type_cache.pop(type_key, None)
            return None
            
        except Exception as e:
            self.logger.error(f"型キャッシュ取得エラー: {e}")
            return None

    def cache_type(self, type_key: str, type_obj: Type) -> None:
        """型のキャッシュ"""
        try:
            self._type_cache[type_key] = weakref.ref(
                type_obj,
                lambda ref: self._type_cache.pop(type_key, None)
            )
        except Exception as e:
            self.logger.error(f"型キャッシュエラー: {e}")

    def get_dict(self) -> dict:
        """dictプールからの取得"""
        return self._dict_pool.acquire()

    def release_dict(self, d: dict) -> None:
        """dictプールへの返却"""
        d.clear()
        self._dict_pool.release(d)

    def get_tuple(self, items=()) -> tuple:
        """tupleプールからの取得"""
        t = self._tuple_pool.acquire()
        return t + tuple(items)

    def release_tuple(self, t: tuple) -> None:
        """tupleプールへの返却"""
        self._tuple_pool.release(t)

    def cleanup(self) -> None:
        """型管理システムのクリーンアップ"""
        try:
            self._type_cache.clear()
            self._dict_pool.cleanup()
            self._tuple_pool.cleanup()
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")
