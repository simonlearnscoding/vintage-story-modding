from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"
    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lives = Column(Integer, nullable=False)

class UserLog(Base):
    __tablename__ = "userlog"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, ForeignKey("players.uid"), nullable=False)
    joinedAt = Column(String, nullable=False)
    leftAt = Column(String, nullable=True)

class DeathInfo(Base):
    __tablename__ = "deathinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, ForeignKey("players.uid"), nullable=False)
    damageSource = Column(String, nullable=False)
    deathTime = Column(String, nullable=False)