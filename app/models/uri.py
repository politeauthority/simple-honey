"""Uri - MODEL

"""
from sqlalchemy import UniqueConstraint, Column, Text, String, DateTime, Integer
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
    meta_val = Column(Text())
    requests = relationship('WebRequest', back_populates="uri")
    hits = Column(Integer, default=0)

    UniqueConstraint('uri', 'domain', name='uix_1')

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.uri)

# End File: simple-honey/app/models/uri.py
