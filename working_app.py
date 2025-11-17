from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select, func
import sys
import os
import uvicorn

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.database import get_engine
from backend.models import Player, PlayerGameStat

app = FastAPI()

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "src", "frontend", "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, stat: str = "passing_yards"):
    engine = get_engine()
    with Session(engine) as session:
        stat_definitions = {
            "passing_yards": {"name": "Passing Yards", "field": PlayerGameStat.passing_yards},
            "rushing_yards": {"name": "Rushing Yards", "field": PlayerGameStat.rushing_yards},
            "receiving_yards": {"name": "Receiving Yards", "field": PlayerGameStat.receiving_yards},
            "pass_tds": {"name": "Passing TDs", "field": PlayerGameStat.pass_tds},
            "rush_tds": {"name": "Rushing TDs", "field": PlayerGameStat.rush_tds},
            "rec_tds": {"name": "Receiving TDs", "field": PlayerGameStat.rec_tds},
            "sacks": {"name": "Sacks", "field": PlayerGameStat.sacks},
            "tackles": {"name": "Tackles", "field": PlayerGameStat.tackles},
            "interceptions": {"name": "Interceptions", "field": PlayerGameStat.interceptions},
            "fgm": {"name": "Field Goals Made", "field": PlayerGameStat.fgm},
            "fantasy_points": {"name": "Fantasy Points", "field": PlayerGameStat.fantasy_points},
        }
        
        current_stat = stat_definitions.get(stat, stat_definitions["passing_yards"])
        
        leaders = session.exec(
            select(
                Player.player_id,
                Player.full_name,
                Player.position,
                PlayerGameStat.team,
                func.sum(current_stat["field"]).label('total_stat')
            )
            .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
            .where(
                (current_stat["field"] > 0) & 
                (PlayerGameStat.season_type == "REG")
            )
            .group_by(Player.player_id, Player.full_name, Player.position, PlayerGameStat.team)
            .order_by(func.sum(current_stat["field"]).desc())
            .limit(20)
        ).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "leaders": leaders,
        "current_stat": current_stat["name"],
        "selected_stat": stat,
        "stat_definitions": stat_definitions
    })

@app.get("/players", response_class=HTMLResponse)
def players_page(request: Request, search: str = None, position: str = None):
    engine = get_engine()
    with Session(engine) as session:
        query = select(Player)
        
        if search:
            query = query.where(Player.full_name.ilike(f"%{search}%"))
        if position:
            query = query.where(Player.position == position)
        
        players = session.exec(query.order_by(Player.full_name).limit(50)).all()
    
    return templates.TemplateResponse("players.html", {
        "request": request,
        "players": players,
        "search_query": search,
        "selected_position": position
    })

@app.get("/player/{player_id}", response_class=HTMLResponse)
def player_detail(request: Request, player_id: str):
    engine = get_engine()
    with Session(engine) as session:
        player = session.exec(select(Player).where(Player.player_id == player_id)).first()
        stats = session.exec(
            select(PlayerGameStat)
            .where(PlayerGameStat.player_id == player_id)
            .order_by(PlayerGameStat.week)
        ).all()
        
        return templates.TemplateResponse("player_detail.html", {
            "request": request,
            "player": player,
            "stats": stats
        })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)