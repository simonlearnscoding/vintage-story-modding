from sqlalchemy import select
from app.models.database import Player, UserLog
from app.models.database_connection import Session
from typing import List, Dict
from datetime import datetime


class PlayerService:
    @staticmethod
    def create_player(uid: str, name: str) -> Player:
        with Session() as session:
            # Check if player already exists
            existing = session.execute(
                select(Player).where(Player.uid == uid)
            ).scalar_one_or_none()

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
            return session.execute(
                select(Player).where(Player.uid == uid)
            ).scalar_one_or_none()

    @staticmethod
    def get_all_players() -> list[Player]:
        with Session() as session:
            return session.execute(select(Player)).scalars().all()

    @staticmethod
    def get_all_player_details() -> list[dict]:
        with Session() as session:
            players = session.execute(select(Player)).scalars().all()
            all_details = []

            for player in players:
                active_log = (
                    session.execute(
                        select(UserLog)
                        .where(UserLog.uid == player.uid, UserLog.leftAt.is_(None))
                        .order_by(UserLog.id.desc())
                    )
                    .scalars()
                    .first()
                )

                last_log = (
                    session.execute(
                        select(UserLog)
                        .where(UserLog.uid == player.uid)
                        .order_by(UserLog.id.desc())
                    )
                    .scalars()
                    .first()
                )

                is_online = active_log is not None
                online_since = None
                last_online = None

                if is_online and active_log:
                    join_time = datetime.strptime(active_log.joinedAt, "%m/%d/%Y %H:%M")
                    now = datetime.now()

                    duration_seconds = (now - join_time).total_seconds()
                    if duration_seconds < 0:
                        duration_seconds = 0

                    hours = int(duration_seconds // 3600)
                    minutes = int((duration_seconds % 3600) // 60)
                    seconds = int(duration_seconds % 60)

                    if seconds > 0:
                        online_since = f"{hours}h {minutes}m {seconds}s"
                    else:
                        online_since = f"{hours}h {minutes}m"

                elif last_log and last_log.leftAt:
                    last_online = last_log.leftAt

                all_details.append(
                    {
                        "name": player.name,
                        "uid": player.uid,
                        "isOnline": is_online,
                        "onlineSince": online_since,
                        "lastOnline": last_online,
                    }
                )

            return all_details

    @staticmethod
    def create_user_log(
        uid: str, joined_at: str, left_at: str | None = None
    ) -> UserLog:
        with Session() as session:
            # Delete any existing log with same uid and no leftAt
            existing_log = session.execute(
                select(UserLog).where(UserLog.uid == uid, UserLog.leftAt.is_(None))
            ).scalar_one_or_none()

            if existing_log:
                session.delete(existing_log)

            log = UserLog(uid=uid, joinedAt=joined_at, leftAt=left_at)
            session.add(log)
            session.commit()
            session.refresh(log)
            return log

    @staticmethod
    def get_player_logs(uid: str) -> list[dict]:
        with Session() as session:
            result = session.execute(
                select(UserLog, Player.name)
                .join(Player, UserLog.uid == Player.uid)
                .where(UserLog.uid == uid)
                .order_by(UserLog.id.desc())
            ).all()

            return [
                {
                    "id": log.id,
                    "uid": log.uid,
                    "name": name,
                    "joinedAt": log.joinedAt,
                    "leftAt": log.leftAt,
                }
                for log, name in result
            ]

    @staticmethod
    def get_player_details(uid: str) -> dict | None:
        with Session() as session:
            player = session.execute(
                select(Player).where(Player.uid == uid)
            ).scalar_one_or_none()

            if not player:
                return None

            active_log = session.execute(
                select(UserLog)
                .where(UserLog.uid == uid, UserLog.leftAt.is_(None))
                .order_by(UserLog.id.desc())
            ).scalar_one_or_none()

            last_log = (
                session.execute(
                    select(UserLog)
                    .where(UserLog.uid == uid)
                    .order_by(UserLog.id.desc())
                )
                .scalars()
                .first()
            )

            is_online = active_log is not None
            online_since = None
            last_online = None

            if is_online and active_log:
                join_time = datetime.strptime(active_log.joinedAt, "%m/%d/%Y %H:%M")
                now = datetime.now()

                duration_seconds = (now - join_time).total_seconds()
                if duration_seconds < 0:
                    duration_seconds = 0

                hours = int(duration_seconds // 3600)
                minutes = int((duration_seconds % 3600) // 60)
                seconds = int(duration_seconds % 60)

                if seconds > 0:
                    online_since = f"{hours}h {minutes}m {seconds}s"
                else:
                    online_since = f"{hours}h {minutes}m"

            elif last_log and last_log.leftAt:
                last_online = last_log.leftAt

            return {
                "name": player.name,
                "uid": player.uid,
                "isOnline": is_online,
                "onlineSince": online_since,
                "lastOnline": last_online,
            }

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
    def get_all_player_logs() -> list[dict]:
        with Session() as session:
            result = session.execute(
                select(UserLog, Player.name)
                .join(Player, UserLog.uid == Player.uid)
                .order_by(UserLog.id.desc())
            ).all()

            return [
                {
                    "id": log.id,
                    "uid": log.uid,
                    "name": name,
                    "joinedAt": log.joinedAt,
                    "leftAt": log.leftAt,
                }
                for log, name in result
            ]
