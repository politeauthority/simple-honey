"""KnownIp - MODEL

"""
from sqlalchemy import Column, Text, String, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class KnownIp(Base):

    __tablename__ = 'known_ips'

    ip = Column(String(100), nullable=False)
    name = Column(String(100))
    last_seen = Column(DateTime)
    notes = Column(Text())
    requests = relationship('WebRequest', back_populates="known_ip")

# End File: simple-honey/app/models/known_ip.py
