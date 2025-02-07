from ..base_tab import BaseTab
import logging

logger = logging.getLogger(__name__)

class DataIOTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.debug("DataIOTab initialized")
