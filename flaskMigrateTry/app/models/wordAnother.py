from app.models.base import db
from sqlalchemy import Column,String,Integer


class CET8(db.Model):
    __tablename__ = 'cet4'
    id = Column(Integer, primary_key=True)
    word=Column(String)
    phonetic=Column(String)
    definition=Column(String)
    translation=Column(String)