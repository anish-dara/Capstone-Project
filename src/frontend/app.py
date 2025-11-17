from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.database import get_engine
from backend.models import Player, PlayerGameStat

app = FastAPI()

# Get the absolute path to static and templates directories
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, session: Session = Depends(get_session), stat: str = "passing_yards"):
    from sqlalchemy import func
    
    # Define all available stats with their display names and positions
    stat_definitions = {
        "passing_yards": {"name": "Passing Yards", "positions": ["QB"], "field": PlayerGameStat.passing_yards},
        "pass_tds": {"name": "Passing TDs", "positions": ["QB"], "field": PlayerGameStat.pass_tds},
        "rushing_yards": {"name": "Rushing Yards", "positions": ["QB", "RB", "WR", "TE"], "field": PlayerGameStat.rushing_yards},
        "rush_tds": {"name": "Rushing TDs", "positions": ["QB", "RB", "WR", "TE"], "field": PlayerGameStat.rush_tds},
        "receiving_yards": {"name": "Receiving Yards", "positions": ["RB", "WR", "TE"], "field": PlayerGameStat.receiving_yards},
        "rec_tds": {"name": "Receiving TDs", "positions": ["RB", "WR", "TE"], "field": PlayerGameStat.rec_tds},
        "receptions": {"name": "Receptions", "positions": ["RB", "WR", "TE"], "field": PlayerGameStat.receptions},
        "sacks": {"name": "Sacks", "positions": ["DE", "LB", "DT", "OLB", "ILB", "DL"], "field": PlayerGameStat.sacks},
        "tackles": {"name": "Tackles", "positions": ["DE", "LB", "DT", "OLB", "ILB", "DL", "DB", "CB", "S"], "field": PlayerGameStat.tackles},
        "interceptions": {"name": "Interceptions", "positions": ["DB", "CB", "S", "LB"], "field": PlayerGameStat.interceptions},
        "fgm": {"name": "Field Goals Made", "positions": ["K"], "field": PlayerGameStat.fgm},
        "fga": {"name": "Field Goals Attempted", "positions": ["K"], "field": PlayerGameStat.fga},
        "fg_percentage": {"name": "Field Goal %", "positions": ["K"], "field": PlayerGameStat.fg_percentage},
        "passing_epa": {"name": "Passing EPA", "positions": ["QB"], "field": PlayerGameStat.passing_epa},
        "def_pass_defended": {"name": "Pass Defended", "positions": ["DB", "CB", "S", "LB"], "field": PlayerGameStat.def_pass_defended},
        "def_fumbles_forced": {"name": "Fumbles Forced", "positions": ["DE", "LB", "DT", "OLB", "ILB", "DL", "DB"], "field": PlayerGameStat.def_fumbles_forced},
        "fantasy_points": {"name": "Fantasy (Standard)", "positions": ["QB", "RB", "WR", "TE", "K"], "field": PlayerGameStat.fantasy_points},
        "fantasy_points_ppr": {"name": "Fantasy (PPR)", "positions": ["QB", "RB", "WR", "TE", "K"], "field": PlayerGameStat.fantasy_points_ppr},
        "rushing_epa": {"name": "Rushing EPA", "positions": ["QB", "RB"], "field": PlayerGameStat.rushing_epa},
        "receiving_epa": {"name": "Receiving EPA", "positions": ["RB", "WR", "TE"], "field": PlayerGameStat.receiving_epa},
    }
    
    # Get current stat definition
    current_stat = stat_definitions.get(stat, stat_definitions["passing_yards"])
    
    # Build query for selected stat
    if stat == "fg_percentage":
        # For percentages, use average and filter for kickers with attempts
        leaders = session.exec(
            select(
                Player.full_name,
                Player.player_id,
                Player.position,
                PlayerGameStat.team,
                func.avg(current_stat["field"]).label('total_stat')
            )
            .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
            .where(
                (PlayerGameStat.fga >= 5) &  # Minimum 5 attempts for qualification
                (PlayerGameStat.season_type == "REG") &
                (Player.position.in_(current_stat["positions"]))
            )
            .group_by(Player.player_id, Player.full_name, Player.position, PlayerGameStat.team)
            .order_by(func.avg(current_stat["field"]).desc())
            .limit(20)
        ).all()
    else:
        # For counting stats, use sum
        leaders = session.exec(
            select(
                Player.full_name,
                Player.player_id,
                Player.position,
                PlayerGameStat.team,
                func.sum(current_stat["field"]).label('total_stat')
            )
            .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
            .where(
                (current_stat["field"] > 0) & 
                (PlayerGameStat.season_type == "REG") &
                (Player.position.in_(current_stat["positions"]))
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
async def players_page(request: Request, session: Session = Depends(get_session), search: str = None, position: str = None):
    from sqlalchemy import func
    
    # Build base query with aggregated stats
    query = select(
        Player.player_id,
        Player.full_name,
        Player.position,
        func.sum(PlayerGameStat.passing_yards).label('total_passing_yards'),
        func.sum(PlayerGameStat.pass_tds).label('total_pass_tds'),
        func.sum(PlayerGameStat.rushing_yards).label('total_rushing_yards'),
        func.sum(PlayerGameStat.rush_tds).label('total_rush_tds'),
        func.sum(PlayerGameStat.receiving_yards).label('total_receiving_yards'),
        func.sum(PlayerGameStat.rec_tds).label('total_rec_tds'),
        func.sum(PlayerGameStat.sacks).label('total_sacks'),
        func.sum(PlayerGameStat.interceptions).label('total_interceptions'),
        func.sum(PlayerGameStat.tackles).label('total_tackles'),
        func.sum(PlayerGameStat.fgm).label('total_fgm'),
        func.sum(PlayerGameStat.fga).label('total_fga'),
        func.sum(PlayerGameStat.punt_returns).label('total_punt_returns'),
        func.sum(PlayerGameStat.punt_return_yards).label('total_punt_return_yards'),
        func.sum(PlayerGameStat.kickoff_returns).label('total_kickoff_returns'),
        func.sum(PlayerGameStat.kickoff_return_yards).label('total_kickoff_return_yards'),
        func.sum(PlayerGameStat.def_fumbles_forced).label('total_fumbles_forced'),
        func.sum(PlayerGameStat.def_pass_defended).label('total_pass_defended')
    ).select_from(
        Player
    ).outerjoin(
        PlayerGameStat, 
        (Player.player_id == PlayerGameStat.player_id) & 
        (PlayerGameStat.season_type == "REG")
    ).group_by(
        Player.player_id, Player.full_name, Player.position
    )
    
    # Apply filters
    if search:
        query = query.where(Player.full_name.ilike(f"%{search}%"))
    if position:
        query = query.where(Player.position == position)
    
    # Add position-specific sorting by primary stat
    if position == "QB":
        query = query.order_by(func.sum(PlayerGameStat.passing_yards).desc())
    elif position == "RB":
        query = query.order_by(func.sum(PlayerGameStat.rushing_yards).desc())
    elif position in ["WR", "TE"]:
        query = query.order_by(func.sum(PlayerGameStat.receiving_yards).desc())
    elif position in ["DE", "LB", "DT", "OLB", "ILB", "DL"]:
        query = query.order_by(func.sum(PlayerGameStat.sacks).desc())
    elif position in ["CB", "S", "FS", "SS", "DB"]:
        query = query.order_by(func.sum(PlayerGameStat.interceptions).desc())
    elif position == "K":
        query = query.order_by(func.sum(PlayerGameStat.fgm).desc())
    elif position == "OL":
        query = query.order_by(func.sum(PlayerGameStat.snaps_played).desc())
    else:
        # Default sort by name for mixed positions or no filter
        query = query.order_by(Player.full_name)
    
    players = session.exec(query.limit(50)).all()
    
    return templates.TemplateResponse("players.html", {
        "request": request,
        "players": players,
        "search_query": search,
        "selected_position": position
    })

@app.get("/player/{player_id}", response_class=HTMLResponse)
async def player_detail(request: Request, player_id: str, session: Session = Depends(get_session)):
    try:
        player = session.exec(select(Player).where(Player.player_id == player_id)).first()
        if not player:
            # Create a dummy player object to avoid template errors
            player = Player(player_id=player_id, full_name="Player Not Found")
        
        stats = session.exec(select(PlayerGameStat).where(PlayerGameStat.player_id == player_id)).all()
        
        return templates.TemplateResponse("player_detail.html", {
            "request": request,
            "player": player,
            "stats": stats
        })
    except Exception as e:
        # Return error page with simple dict
        class DummyPlayer:
            def __init__(self, player_id, full_name):
                self.player_id = player_id
                self.full_name = full_name
                self.position = None
        
        return templates.TemplateResponse("player_detail.html", {
            "request": request,
            "player": DummyPlayer(player_id, "Error Loading Player"),
            "stats": [],
            "error": str(e)
        })