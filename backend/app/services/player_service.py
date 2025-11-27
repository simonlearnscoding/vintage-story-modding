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
    
    @staticmethod
    def get_player_logs(uid: str) -> list[UserLog]:
        with Session() as session:
            return session.execute(select(UserLog).where(UserLog.uid == uid).order_by(UserLog.id.desc())).scalars().all()
    
    @staticmethod
    def update_user_log_with_leave_time(uid: str, left_at: str) -> UserLog | None:
        with Session() as session:
            # Find the most recent log for this user with no leftAt time
            log = session.execute(
                select(UserLog)
                .where(UserLog.uid == uid, UserLog.leftAt.is_(None))
                .order_by(UserLog.id.desc())
            ).scalar_one_or_none()
            
            if log:
                log.leftAt = left_at
                session.commit()
                session.refresh(log)
                return log
            return None
    
    @staticmethod
    def get_all_player_logs() -> list[UserLog]:
        with Session() as session:
            return session.execute(select(UserLog).order_by(UserLog.id.desc())).scalars().all()