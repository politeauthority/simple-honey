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

# End File: simple-honey/app/models/redirection.py
