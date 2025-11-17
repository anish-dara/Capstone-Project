from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from .database import get_engine
from .models import Player, PlayerGameStat

app = FastAPI(title="Sports Database API")

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

@app.get("/players")
def get_players(session: Session = Depends(get_session)):
    return session.exec(select(Player)).all()

@app.get("/players/{player_id}")
def get_player(player_id: str, session: Session = Depends(get_session)):
    return session.exec(select(Player).where(Player.player_id == player_id)).first()

@app.get("/stats")
def get_stats(season: int = None, session: Session = Depends(get_session)):
    query = select(PlayerGameStat)
    if season:
        query = query.where(PlayerGameStat.season == season)
    return session.exec(query).all()

@app.get("/stats/{player_id}")
def get_player_stats(player_id: str, session: Session = Depends(get_session)):
    return session.exec(select(PlayerGameStat).where(PlayerGameStat.player_id == player_id)).all()

@app.get("/search/players")
def search_players(name: str, session: Session = Depends(get_session)):
    return session.exec(select(Player).where(Player.full_name.contains(name))).all()