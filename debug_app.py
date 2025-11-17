from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.get("/test-imports")
def test_imports():
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from backend.database import get_engine
        from backend.models import Player, PlayerGameStat
        return {"status": "imports work"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/test-db")
def test_db():
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from backend.database import get_engine
        from backend.models import Player
        from sqlmodel import Session, select
        
        engine = get_engine()
        with Session(engine) as session:
            count = len(session.exec(select(Player)).all())
        return {"status": "database works", "player_count": count}
    except Exception as e:
        return {"error": str(e)}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from backend.database import get_engine
        from backend.models import Player, PlayerGameStat
        from sqlmodel import Session, select, func
        
        engine = get_engine()
        with Session(engine) as session:
            leaders = session.exec(
                select(
                    Player.full_name,
                    Player.position,
                    PlayerGameStat.team,
                    func.sum(PlayerGameStat.passing_yards).label('total_yards')
                )
                .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                .where(PlayerGameStat.passing_yards > 0)
                .group_by(Player.player_id, Player.full_name, Player.position, PlayerGameStat.team)
                .order_by(func.sum(PlayerGameStat.passing_yards).desc())
                .limit(10)
            ).all()
        
        html = """
        <html>
        <head><title>NFL Dashboard</title></head>
        <body>
        <h1>NFL Passing Leaders</h1>
        <table border="1">
        <tr><th>Player</th><th>Position</th><th>Team</th><th>Yards</th></tr>
        """
        
        for leader in leaders:
            html += f"<tr><td>{leader.full_name}</td><td>{leader.position}</td><td>{leader.team}</td><td>{leader.total_yards:.0f}</td></tr>"
        
        html += "</table></body></html>"
        return html
        
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)