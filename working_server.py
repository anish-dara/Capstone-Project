from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from backend.database import get_engine
    from backend.models import Player, PlayerGameStat
    from sqlmodel import Session, select, func
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NFL Dashboard Running", "endpoints": ["/dashboard", "/players"]}

@app.get("/players", response_class=HTMLResponse)
def players_list():
    if not DB_AVAILABLE:
        return """<html><body><h1>Players</h1><p>Database not available</p></body></html>"""
    
    try:
        engine = get_engine()
        with Session(engine) as session:
            players = session.exec(
                select(Player.player_id, Player.full_name, Player.position, Player.team)
                .order_by(Player.full_name)
                .limit(50)
            ).all()
        
        html = """<html><body style="font-family: Arial; margin: 40px;">
        <h1>NFL Players</h1>
        <p><a href="/dashboard">← Back to Dashboard</a></p>
        <table border="1" style="border-collapse: collapse;">
        <tr><th>Player</th><th>Position</th><th>Team</th><th>Details</th></tr>"""
        
        for player in players:
            html += f"""<tr>
                <td>{player.full_name}</td>
                <td>{player.position or 'N/A'}</td>
                <td>{player.team or 'N/A'}</td>
                <td><a href="/player/{player.player_id}">View Stats</a></td>
            </tr>"""
        
        html += "</table></body></html>"
        return html
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"

@app.get("/player/{player_id}", response_class=HTMLResponse)
def player_detail(player_id: str):
    if not DB_AVAILABLE:
        return """<html><body><h1>Player Detail</h1><p>Database not available</p></body></html>"""
    
    try:
        engine = get_engine()
        with Session(engine) as session:
            player = session.exec(
                select(Player).where(Player.player_id == player_id)
            ).first()
            
            if not player:
                return "<html><body><h1>Player Not Found</h1></body></html>"
            
            stats = session.exec(
                select(PlayerGameStat)
                .where((PlayerGameStat.player_id == player_id) & (PlayerGameStat.season_type == "REG"))
                .limit(10)
            ).all()
        
        html = f"""<html><body style="font-family: Arial; margin: 40px;">
        <h1>{player.full_name}</h1>
        <p><strong>Position:</strong> {player.position or 'N/A'} | <strong>Team:</strong> {player.team or 'N/A'}</p>
        <p><a href="/players">← Back to Players</a> | <a href="/dashboard">Dashboard</a></p>
        <h2>Recent Game Stats</h2>
        <table border="1" style="border-collapse: collapse;">
        <tr><th>Week</th><th>Opponent</th><th>Pass Yds</th><th>Rush Yds</th><th>Receptions</th><th>Sacks</th></tr>"""
        
        for stat in stats:
            html += f"""<tr>
                <td>{getattr(stat, 'week', 'N/A')}</td>
                <td>{getattr(stat, 'opponent_team', 'N/A')}</td>
                <td>{getattr(stat, 'passing_yards', 0) or 0}</td>
                <td>{getattr(stat, 'rushing_yards', 0) or 0}</td>
                <td>{getattr(stat, 'receptions', 0) or 0}</td>
                <td>{getattr(stat, 'sacks', 0) or 0}</td>
            </tr>"""
        
        html += "</table></body></html>"
        return html
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p><p><a href='/players'>Back to Players</a></p></body></html>"

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(stat: str = "passing_yards"):
    if not DB_AVAILABLE:
        return """<html><body><h1>NFL Dashboard</h1><p>Database not available</p></body></html>"""
    
    try:
        engine = get_engine()
        with Session(engine) as session:
            if stat == "receptions":
                leaders = session.exec(
                    select(Player.full_name, PlayerGameStat.team, func.sum(PlayerGameStat.receptions).label('total'))
                    .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                    .where((PlayerGameStat.receptions > 0) & (PlayerGameStat.season_type == "REG"))
                    .group_by(Player.player_id, Player.full_name, PlayerGameStat.team)
                    .order_by(func.sum(PlayerGameStat.receptions).desc())
                    .limit(10)
                ).all()
                title = "Reception Leaders"
            elif stat == "sacks":
                leaders = session.exec(
                    select(Player.full_name, PlayerGameStat.team, func.sum(PlayerGameStat.sacks).label('total'))
                    .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                    .where((PlayerGameStat.sacks > 0) & (PlayerGameStat.season_type == "REG"))
                    .group_by(Player.player_id, Player.full_name, PlayerGameStat.team)
                    .order_by(func.sum(PlayerGameStat.sacks).desc())
                    .limit(10)
                ).all()
                title = "Sack Leaders"
            else:
                leaders = session.exec(
                    select(Player.full_name, PlayerGameStat.team, func.sum(PlayerGameStat.passing_yards).label('total'))
                    .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
                    .where((PlayerGameStat.passing_yards > 0) & (PlayerGameStat.season_type == "REG"))
                    .group_by(Player.player_id, Player.full_name, PlayerGameStat.team)
                    .order_by(func.sum(PlayerGameStat.passing_yards).desc())
                    .limit(10)
                ).all()
                title = "Passing Yards Leaders"
        
        html = f"""<html><body style="font-family: Arial; margin: 40px;">
        <h1>{title}</h1>
        <p>
            <a href="/dashboard">Passing Yards</a> | 
            <a href="/dashboard?stat=receptions">Receptions</a> | 
            <a href="/dashboard?stat=sacks">Sacks</a> | 
            <a href="/players">All Players</a>
        </p>
        <table border="1" style="border-collapse: collapse;">
        <tr><th>Rank</th><th>Player</th><th>Team</th><th>{title.split()[0]}</th></tr>"""
        
        for i, leader in enumerate(leaders, 1):
            html += f"<tr><td>{i}</td><td>{leader.full_name}</td><td>{leader.team}</td><td>{leader.total:.1f}</td></tr>"
        
        html += "</table></body></html>"
        return html
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)