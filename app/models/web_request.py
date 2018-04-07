"""WebRequest - MODEL

"""
from sqlalchemy import Column, String, PickleType, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class WebRequest(Base):

    __tablename__ = 'web_requests'

    uri = Column(Text(), nullable=False)
    data = Column(PickleType())
    user_agent = Column(String(250))
    request_type = Column(String(10))
    ip = Column(String(50))
    platform = Column(String(100))
    browser_name = Column(String(100))
    browser_version = Column(String(150))
    browser_language = Column(String(50))
    notes = Column(Text())
    known_id = Column(Integer, ForeignKey('known_ips.id'))
    known_ip = relationship("KnownIp", back_populates="requests")
    uri_id = Column(Integer, ForeignKey('uris.id'))
    uri = relationship("Uri", back_populates="requests")

# End File: simple-honey/app/models/web_request.py
