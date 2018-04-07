"""Uri - MODEL

"""
from sqlalchemy import Column, Text, String, DateTime, PickleType
from sqlalchemy.orm import relationship

from app.models.base import Base


class Uri(Base):

    __tablename__ = 'uris'

    uri = Column(Text(), nullable=False)
    domain = Column(String(250))
    name = Column(String(100))
    last_hit = Column(DateTime)
    notes = Column(Text())
    response_type = Column(String(100))
    meta = Column(PickleType())
    requests = relationship('WebRequest', back_populates="uri")

# End File: simple-honey/app/models/uri.py
