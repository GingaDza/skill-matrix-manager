from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    """タイムスタンプ機能を提供するMixin"""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        if not 'created_at' in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if not 'updated_at' in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        super().__init__(*args, **kwargs)