"""WebRequest - MODEL

"""
from sqlalchemy import Column, String, PickleType, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class WebRequest(Base):

    __tablename__ = 'web_requests'

    data = Column(PickleType())
    domain = Column(String(250))
    user_agent = Column(String(250))
    request_type = Column(String(10))
    platform = Column(String(100))
    browser_name = Column(String(100))
    browser_version = Column(String(150))
    browser_language = Column(String(50))
    notes = Column(Text())
    ip_id = Column(Integer, ForeignKey('known_ips.id'))
    ip = relationship("KnownIp", back_populates="requests")
    uri_id = Column(Integer, ForeignKey('uris.id'))
    uri = relationship("Uri", back_populates="requests")

# End File: simple-honey/app/models/web_request.py
