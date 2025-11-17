from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.database import get_engine
from backend.models import Player, PlayerGameStat
from sqlmodel import Session, select, func

app = FastAPI()

@app.get("/test/{stat}")
def test_stat(stat: str):
    engine = get_engine()
    with Session(engine) as session:
        if stat == "receptions":
            leaders = session.exec(
                select(
                    Player.full_name,
                    func.sum(PlayerGameStat.receptions).label('total')
                )
                .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                .where(PlayerGameStat.receptions > 0)
                .group_by(Player.player_id, Player.full_name)
                .order_by(func.sum(PlayerGameStat.receptions).desc())
                .limit(5)
            ).all()
        elif stat == "fga":
            leaders = session.exec(
                select(
                    Player.full_name,
                    func.sum(PlayerGameStat.fga).label('total')
                )
                .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                .where(PlayerGameStat.fga > 0)
                .group_by(Player.player_id, Player.full_name)
                .order_by(func.sum(PlayerGameStat.fga).desc())
                .limit(5)
            ).all()
        else:
            return {"error": "Invalid stat"}
        
        return {"stat": stat, "leaders": [{"name": l.full_name, "total": l.total} for l in leaders]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)