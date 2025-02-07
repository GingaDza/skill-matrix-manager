import sqlite3
from typing import Optional

class Database:
    _instance: Optional['Database'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __init__(self):
        self._db_path = "skillmatrix.db"

    @classmethod
    def get_instance(cls) -> 'Database':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_connection_string(self) -> str:
        return f"sqlite:///{self._db_path}"

    def get_connection(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
        return self._connection

db = Database.get_instance()