from fastapi import FastAPI
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.database import get_engine
from backend.models import Player, PlayerGameStat
from sqlmodel import Session, select, func

app = FastAPI()

@app.get("/test/{stat}")
def test_individual_stat(stat: str):
    engine = get_engine()
    with Session(engine) as session:
        if stat == "receptions":
            leaders = session.exec(
                select(
                    Player.full_name,
                    func.sum(PlayerGameStat.receptions).label('total')
                )
                .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                .where((PlayerGameStat.receptions > 0) & (PlayerGameStat.season_type == "REG"))
                .group_by(Player.player_id, Player.full_name)
                .order_by(func.sum(PlayerGameStat.receptions).desc())
                .limit(5)
            ).all()
        elif stat == "passing_epa":
            leaders = session.exec(
                select(
                    Player.full_name,
                    func.sum(PlayerGameStat.passing_epa).label('total')
                )
                .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                .where((PlayerGameStat.passing_epa.isnot(None)) & (PlayerGameStat.season_type == "REG"))
                .group_by(Player.player_id, Player.full_name)
                .order_by(func.sum(PlayerGameStat.passing_epa).desc())
                .limit(5)
            ).all()
        elif stat == "sacks":
            leaders = session.exec(
                select(
                    Player.full_name,
                    func.sum(PlayerGameStat.sacks).label('total')
                )
                .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                .where((PlayerGameStat.sacks > 0) & (PlayerGameStat.season_type == "REG"))
                .group_by(Player.player_id, Player.full_name)
                .order_by(func.sum(PlayerGameStat.sacks).desc())
                .limit(5)
            ).all()
        else:
            return {"error": "Test passing_yards, receptions, passing_epa, or sacks"}
        
        return {
            "stat": stat,
            "leaders": [{"name": l.full_name, "total": float(l.total) if l.total else 0} for l in leaders]
        }

if __name__ == "__main__":
    print("Test individual stats at:")
    print("http://127.0.0.1:8000/test/receptions")
    print("http://127.0.0.1:8000/test/passing_epa") 
    print("http://127.0.0.1:8000/test/sacks")
    uvicorn.run(app, host="127.0.0.1", port=8000)