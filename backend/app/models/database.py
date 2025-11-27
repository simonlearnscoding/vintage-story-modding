from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"
    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class UserLog(Base):
    __tablename__ = "userlog"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, ForeignKey("players.uid"), nullable=False)
    joinedAt = Column(String, nullable=False)
    leftAt = Column(String, nullable=True)