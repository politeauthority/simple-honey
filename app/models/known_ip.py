"""Known Ip - MODEL

"""
from sqlalchemy import Column, Text, String, DateTime

from app.models.base import Base


class KnownIp(Base):

    __tablename__ = 'known_ips'

    ip = Column(String(100), nullable=False)
    name = Column(String(100))
    last_seen = Column(DateTime)
    notes = Column(Text())

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            r = self.query.filter(KnownIp.id == self.id).one()
            if r:
                self._build_obj(r)

    def _build_obj(self, obj):
        self.id = int(obj.id)
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.ip = obj.ip
        self.name = obj.name
        self.last_seen = obj.last_seen
        self.notes = obj.notes

# End File: simple-honey/app/models/known_ip.py
