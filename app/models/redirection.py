"""Redirection - MODEL

"""
from sqlalchemy import Column, Text, Integer

from app.models.base import Base


class Redirection(Base):

    __tablename__ = 'redirections'

    uri = Column(Text(), nullable=False)
    redirect_url = Column(Text(), nullable=False)
    hits = Column(Integer())
    notes = Column(Text())

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            r = self.query.filter(Redirection.id == self.id).one()
            if r:
                self._build_obj(r)

    def _build_obj(self, obj):
        self.id = int(obj.id)
        self.ts_created = obj.data
        self.ts_updated = obj.ts_updated
        self.uri = obj.uri
        self.redirect_url = obj.redirect_url
        self.hits = obj.hits
        self.notes = obj.notes

# End File: simple-honey/app/models/redirection.py
