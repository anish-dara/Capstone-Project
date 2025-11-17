from sqlmodel import Session, select
try:
    from .models import Player, PlayerGameStat
except ImportError:
    from models import Player, PlayerGameStat

def upsert_player(session: Session, player: Player):
    existing = session.exec(select(Player).where(Player.player_id == player.player_id)).first()
    if existing:
        for key, value in player.dict(exclude_unset=True).items():
            if key != "id":
                setattr(existing, key, value)
    else:
        session.add(player)
    session.commit()

def upsert_player_game_stat(session: Session, stat: PlayerGameStat):
    existing = session.exec(
        select(PlayerGameStat).where(
            PlayerGameStat.player_id == stat.player_id,
            PlayerGameStat.season == stat.season,
            PlayerGameStat.game_id == stat.game_id
        )
    ).first()
    if existing:
        for key, value in stat.dict(exclude_unset=True).items():
            if key != "id":
                setattr(existing, key, value)
    else:
        session.add(stat)
    session.commit()

def get_players(session: Session, limit: int = 100):
    return session.exec(select(Player).limit(limit)).all()