from sqlalchemy import select
from app.models.database import Player, UserLog
from app.models.database_connection import Session

class PlayerService:
    @staticmethod
    def create_player(uid: str, name: str) -> Player:
        with Session() as session:
            # Check if player already exists
            existing = session.execute(select(Player).where(Player.uid == uid)).scalar_one_or_none()
            
            if existing:
                # Update name if changed
                if existing.name != name:
                    existing.name = name
                return existing
            
            # Create new player
            new_player = Player(uid=uid, name=name)
            session.add(new_player)
            session.commit()
            session.refresh(new_player)
            return new_player
    
    @staticmethod
    def get_player(uid: str) -> Player | None:
        with Session() as session:
            return session.execute(select(Player).where(Player.uid == uid)).scalar_one_or_none()
    
    @staticmethod
    def get_all_players() -> list[Player]:
        with Session() as session:
            return session.execute(select(Player)).scalars().all()
    
    @staticmethod
    def create_user_log(uid: str, joined_at: str, left_at: str = None) -> UserLog:
        with Session() as session:
            log = UserLog(uid=uid, joinedAt=joined_at, leftAt=left_at)
            session.add(log)
            session.commit()
            session.refresh(log)
            return log