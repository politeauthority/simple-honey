"""WebRequest - MODEL

"""
from sqlalchemy import Column, String, PickleType, Text

from app.models.base import Base


class WebRequest(Base):

    __tablename__ = 'web_requests'

    uri = Column(Text(), nullable=False)
    data = Column(PickleType())
    user_agent = Column(String(250))
    request_type = Column(String(10))
    ip = Column(String(50))
    notes = Column(Text())

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            c = self.query.filter(WebRequest.id == self.id).one()
            if c:
                self._build_obj(c)

    def _build_obj(self, obj):
        self.id = int(obj.id)
        self.uri = obj.uri
        self.data = obj.data
        self.user_agent = obj.user_agent
        self.ip = obj.ip
        self.request_type = obj.request_type
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.notes = obj.notes

# End File: simple-honey/app/controllers/web_request.py
