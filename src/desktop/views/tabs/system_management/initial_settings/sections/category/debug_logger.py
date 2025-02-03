import logging
from datetime import datetime

class DebugLogger:
    def __init__(self):
        self.current_time = datetime(2025, 2, 3, 18, 44, 15)
        self.current_user = "GingaDza"
        self._debug_call_count = 0
        
    def log_debug(self, message):
        logging.debug(f"{self.current_time} - {self.current_user} {message}")
        
    def log_info(self, message):
        logging.info(f"{self.current_time} - {self.current_user} {message}")
        
    def log_error(self, message, exc_info=None):
        logging.error(f"{self.current_time} - {self.current_user} {message}")
        if exc_info:
            logging.exception("Detailed traceback:")
        
    def log_method_call(self, method_name, **kwargs):
        self._debug_call_count += 1
        self.log_debug(f"Method call #{self._debug_call_count}: {method_name}")
        if kwargs:
            self.log_debug(f"Arguments: {kwargs}")