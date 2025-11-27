from fastapi import FastAPI, Request
from sqlalchemy import Column, Integer, String, create_engine, select, update, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import json

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__= "players"
    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class UserLog(Base):
    __tablename__="userlog"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, ForeignKey("players.uid"), nullable=False)
    joinedAt = Column(String, nullable=False)
    leftAt = Column(String, nullable=True)

engine = create_engine("sqlite:///vintagestorydata.db", echo=True, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI()

@app.post("/join")
async def join(request: Request):
    data = await request.json()      
    uid = data.get("uid")
    name = data.get("playerName")
    joined = data.get("joinedAt")

    with Session() as session:
        sql = select(Player).where(Player.uid == uid)
        result = session.execute(sql).scalar_one_or_none()

        if result:
            # If name is changed update it here
            if result.name != name:
                result.name = name  

        else:
            new_player:Player = Player(uid=uid, name=name)
            session.add(new_player)
            
        log = UserLog(uid=uid, joinedAt=joined)
        session.add(log)
        session.commit()

    return {"status": "received"}



@app.post("/disconnect")
async def disconnect(request: Request):
    body = await request.body()     
    body_str:str = body.decode("utf-8")
    data = json.loads(body_str)
    uid = data.get("uid")
    disconnected = data.get("disconnectedAt")



    return {"status": "received"}
