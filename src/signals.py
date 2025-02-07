from PyQt6.QtCore import QObject, pyqtSignal

class Signals(QObject):
    group_changed = pyqtSignal()
    category_changed = pyqtSignal()
    data_updated = pyqtSignal()
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
