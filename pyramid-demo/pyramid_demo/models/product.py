import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from .. import enums

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
)

from .meta import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    category = Column(Integer, default=enums.product.Category.FOOD.value)
    status = Column(String(1), default=enums.product.Status.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    @hybrid_property
    def actived(self):
        return self.status == enums.product.Status.ACTIVE.value
