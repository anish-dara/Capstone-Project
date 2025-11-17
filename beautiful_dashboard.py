from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.database import get_engine
from backend.models import Player, PlayerGameStat
from sqlmodel import Session, select, func

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NFL Dashboard", "endpoints": ["/dashboard", "/players"]}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(stat: str = "passing_yards"):
    engine = get_engine()
    with Session(engine) as session:
        if stat == "receptions":
            field = PlayerGameStat.receptions
            stat_name = "Receptions"
        elif stat == "sacks":
            field = PlayerGameStat.sacks
            stat_name = "Sacks"
        elif stat == "rushing_yards":
            field = PlayerGameStat.rushing_yards
            stat_name = "Rushing Yards"
        elif stat == "receiving_yards":
            field = PlayerGameStat.receiving_yards
            stat_name = "Receiving Yards"
        elif stat == "pass_tds":
            field = PlayerGameStat.pass_tds
            stat_name = "Passing TDs"
        elif stat == "rush_tds":
            field = PlayerGameStat.rush_tds
            stat_name = "Rushing TDs"
        elif stat == "rec_tds":
            field = PlayerGameStat.rec_tds
            stat_name = "Receiving TDs"
        elif stat == "tackles":
            field = PlayerGameStat.tackles
            stat_name = "Tackles"
        elif stat == "interceptions":
            field = PlayerGameStat.interceptions
            stat_name = "Interceptions"
        elif stat == "fgm":
            field = PlayerGameStat.fgm
            stat_name = "Field Goals Made"
        elif stat == "fantasy_points":
            field = PlayerGameStat.fantasy_points
            stat_name = "Fantasy Points"
        elif stat == "passing_epa":
            field = PlayerGameStat.passing_epa
            stat_name = "Passing EPA"
        elif stat == "rushing_epa":
            field = PlayerGameStat.rushing_epa
            stat_name = "Rushing EPA"
        elif stat == "receiving_epa":
            field = PlayerGameStat.receiving_epa
            stat_name = "Receiving EPA"
        else:
            field = PlayerGameStat.passing_yards
            stat_name = "Passing Yards"
        
        if "epa" in stat:
            condition = field.isnot(None)
        else:
            condition = field > 0
            
        leaders = session.exec(
            select(
                Player.player_id,
                Player.full_name,
                Player.position,
                PlayerGameStat.team,
                func.sum(field).label('total_stat')
            )
            .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
            .where(condition & (PlayerGameStat.season_type == "REG"))
            .group_by(Player.player_id, Player.full_name, Player.position, PlayerGameStat.team)
            .order_by(func.sum(field).desc())
            .limit(20)
        ).all()
        
        title = stat_name + " Leaders"
    
    html = f"""<html>
    <head>
        <title>NFL Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .header {{ background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
            .nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
            .nav h1 {{ color: #2d3748; margin: 0; font-size: 2.5em; font-weight: 700; }}
            .nav-links {{ display: flex; gap: 20px; }}
            .nav-links a {{ background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: 600; }}
            .stat-selector {{ background: rgba(255,255,255,0.9); padding: 20px; border-radius: 12px; text-align: center; }}
            .main-content {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; }}
            td {{ padding: 14px 16px; border-bottom: 1px solid #e2e8f0; }}
            tr:nth-child(even) {{ background: #f7fafc; }}
            .player-link {{ color: #4299e1; text-decoration: none; font-weight: 600; }}
            .rank {{ background: #667eea; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="nav">
                    <h1>NFL Dashboard</h1>
                    <div class="nav-links">
                        <a href="/dashboard">Stats</a>
                        <a href="/players">Players</a>
                    </div>
                </div>
                <div class="stat-selector">
                    <label for="stat-dropdown" style="font-weight: 600; margin-right: 10px;">Select Stat Category:</label>
                    <select id="stat-dropdown" onchange="window.location.href='/dashboard?stat=' + this.value" style="padding: 10px; border-radius: 8px; border: 2px solid #e2e8f0; font-size: 1em; min-width: 200px;">
                        <optgroup label="Offensive Stats">
                            <option value="passing_yards" {'selected' if stat == 'passing_yards' else ''}>Passing Yards</option>
                            <option value="rushing_yards" {'selected' if stat == 'rushing_yards' else ''}>Rushing Yards</option>
                            <option value="receiving_yards" {'selected' if stat == 'receiving_yards' else ''}>Receiving Yards</option>
                            <option value="receptions" {'selected' if stat == 'receptions' else ''}>Receptions</option>
                            <option value="pass_tds" {'selected' if stat == 'pass_tds' else ''}>Passing TDs</option>
                            <option value="rush_tds" {'selected' if stat == 'rush_tds' else ''}>Rushing TDs</option>
                            <option value="rec_tds" {'selected' if stat == 'rec_tds' else ''}>Receiving TDs</option>
                        </optgroup>
                        <optgroup label="Defensive Stats">
                            <option value="sacks" {'selected' if stat == 'sacks' else ''}>Sacks</option>
                            <option value="tackles" {'selected' if stat == 'tackles' else ''}>Tackles</option>
                            <option value="interceptions" {'selected' if stat == 'interceptions' else ''}>Interceptions</option>
                        </optgroup>
                        <optgroup label="EPA Stats">
                            <option value="passing_epa" {'selected' if stat == 'passing_epa' else ''}>Passing EPA</option>
                            <option value="rushing_epa" {'selected' if stat == 'rushing_epa' else ''}>Rushing EPA</option>
                            <option value="receiving_epa" {'selected' if stat == 'receiving_epa' else ''}>Receiving EPA</option>
                        </optgroup>
                        <optgroup label="Special & Fantasy">
                            <option value="fgm" {'selected' if stat == 'fgm' else ''}>Field Goals Made</option>
                            <option value="fantasy_points" {'selected' if stat == 'fantasy_points' else ''}>Fantasy Points</option>
                        </optgroup>
                    </select>
                </div>
            </div>
            <div class="main-content">
                <h2>{title}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Player</th>
                            <th>Position</th>
                            <th>Team</th>
                            <th>{stat_name}</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for i, leader in enumerate(leaders, 1):
        html += f"""<tr>
            <td><div class="rank">{i}</div></td>
            <td><a href="/player/{leader.player_id}" class="player-link">{leader.full_name}</a></td>
            <td style="text-align: center;">{getattr(leader, 'position', 'N/A') or 'N/A'}</td>
            <td style="text-align: center;">{leader.team}</td>
            <td style="text-align: center; font-weight: bold;">{leader.total_stat:.1f}</td>
        </tr>"""
    
    html += """</tbody></table></div></div></body></html>"""
    return html

@app.get("/players", response_class=HTMLResponse)
def players_list(search: str = None, position: str = None):
    try:
        engine = get_engine()
        with Session(engine) as session:
            query = select(Player.player_id, Player.full_name, Player.position)
            
            if search:
                query = query.where(Player.full_name.ilike(f"%{search}%"))
            if position:
                query = query.where(Player.position == position)
            
            players = session.exec(query.order_by(Player.full_name).limit(100)).all()
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"
    
    html = f"""<html>
    <head>
        <title>NFL Players</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .header {{ background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; }}
            .nav {{ display: flex; justify-content: space-between; align-items: center; }}
            .nav h1 {{ color: #2d3748; margin: 0; font-size: 2.5em; }}
            .nav-links a {{ background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-left: 10px; }}
            .search-section {{ background: rgba(255,255,255,0.9); padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
            .main-content {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; }}
            td {{ padding: 14px 16px; border-bottom: 1px solid #e2e8f0; }}
            tr:nth-child(even) {{ background: #f7fafc; }}
            .player-link {{ color: #4299e1; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="nav">
                    <h1>NFL Players</h1>
                    <div class="nav-links">
                        <a href="/dashboard">Stats</a>
                        <a href="/players">Players</a>
                    </div>
                </div>
                <div class="search-section">
                    <form method="get">
                        <input type="text" name="search" placeholder="Search players..." value="{search or ''}" style="padding: 10px; margin-right: 10px;">
                        <select name="position" style="padding: 10px; margin-right: 10px;">
                            <option value="">All Positions</option>
                            <option value="QB" {'selected' if position == 'QB' else ''}>QB</option>
                            <option value="RB" {'selected' if position == 'RB' else ''}>RB</option>
                            <option value="WR" {'selected' if position == 'WR' else ''}>WR</option>
                            <option value="TE" {'selected' if position == 'TE' else ''}>TE</option>
                            <option value="K" {'selected' if position == 'K' else ''}>K</option>
                        </select>
                        <button type="submit" style="padding: 10px 20px; background: #4299e1; color: white; border: none; border-radius: 5px;">Search</button>
                    </form>
                </div>
            </div>
            <div class="main-content">
                <table>
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Position</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for player in players:
        html += f"""<tr>
            <td><strong>{player.full_name}</strong></td>
            <td style="text-align: center;">{player.position or 'N/A'}</td>
            <td style="text-align: center;"><a href="/player/{player.player_id}" class="player-link">View Stats</a></td>
        </tr>"""
    
    html += """</tbody></table></div></div></body></html>"""
    return html

@app.get("/player/{player_id}", response_class=HTMLResponse)
def player_detail(player_id: str):
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
                .limit(17)
            ).all()
            
            # Calculate season totals
            totals = {
                'passing_yards': sum(getattr(s, 'passing_yards', 0) or 0 for s in stats),
                'rushing_yards': sum(getattr(s, 'rushing_yards', 0) or 0 for s in stats),
                'receiving_yards': sum(getattr(s, 'receiving_yards', 0) or 0 for s in stats),
                'receptions': sum(getattr(s, 'receptions', 0) or 0 for s in stats),
                'pass_tds': sum(getattr(s, 'pass_tds', 0) or 0 for s in stats),
                'rush_tds': sum(getattr(s, 'rush_tds', 0) or 0 for s in stats),
                'rec_tds': sum(getattr(s, 'rec_tds', 0) or 0 for s in stats),
                'sacks': sum(getattr(s, 'sacks', 0) or 0 for s in stats),
                'tackles': sum(getattr(s, 'tackles', 0) or 0 for s in stats),
                'interceptions': sum(getattr(s, 'interceptions', 0) or 0 for s in stats),
                'fgm': sum(getattr(s, 'fgm', 0) or 0 for s in stats),
                'fga': sum(getattr(s, 'fga', 0) or 0 for s in stats),
                'fantasy_points': sum(getattr(s, 'fantasy_points', 0) or 0 for s in stats),
                'fantasy_points_ppr': sum(getattr(s, 'fantasy_points_ppr', 0) or 0 for s in stats),
                'passing_epa': sum(getattr(s, 'passing_epa', 0) or 0 for s in stats),
                'rushing_epa': sum(getattr(s, 'rushing_epa', 0) or 0 for s in stats),
                'receiving_epa': sum(getattr(s, 'receiving_epa', 0) or 0 for s in stats)
            }
        
        html = f"""<html>
        <head>
            <title>{player.full_name} - NFL Stats</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
                .header {{ background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; }}
                .nav {{ display: flex; justify-content: space-between; align-items: center; }}
                .nav h1 {{ color: #2d3748; margin: 0; font-size: 2.5em; }}
                .nav-links a {{ background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-left: 10px; }}
                .stats-summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
                .stat-box {{ background: #4299e1; color: white; padding: 15px; border-radius: 10px; text-align: center; }}
                .stat-box .value {{ font-size: 1.5em; font-weight: bold; }}
                .stat-box .label {{ font-size: 0.9em; opacity: 0.9; }}
                .main-content {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }}
                table {{ width: 100%; border-collapse: collapse; font-size: 0.9em; }}
                th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px; text-align: center; }}
                td {{ padding: 6px 8px; border-bottom: 1px solid #e2e8f0; text-align: center; }}
                tr:nth-child(even) {{ background: #f7fafc; }}
                .section {{ margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="nav">
                        <h1>{player.full_name}</h1>
                        <div class="nav-links">
                            <a href="/players">← Players</a>
                            <a href="/dashboard">Dashboard</a>
                        </div>
                    </div>
                    <p><strong>Position:</strong> {player.position or 'N/A'}</p>
                    
                    <div class="stats-summary">
                        <div class="stat-box">
                            <div class="value">{totals['passing_yards']:.0f}</div>
                            <div class="label">Pass Yards</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['rushing_yards']:.0f}</div>
                            <div class="label">Rush Yards</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['receiving_yards']:.0f}</div>
                            <div class="label">Rec Yards</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['receptions']:.0f}</div>
                            <div class="label">Receptions</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['pass_tds'] + totals['rush_tds'] + totals['rec_tds']:.0f}</div>
                            <div class="label">Total TDs</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['sacks']:.1f}</div>
                            <div class="label">Sacks</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['tackles']:.0f}</div>
                            <div class="label">Tackles</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['fantasy_points']:.1f}</div>
                            <div class="label">Fantasy Pts</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['passing_epa']:.1f}</div>
                            <div class="label">Pass EPA</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['rushing_epa']:.1f}</div>
                            <div class="label">Rush EPA</div>
                        </div>
                        <div class="stat-box">
                            <div class="value">{totals['receiving_epa']:.1f}</div>
                            <div class="label">Rec EPA</div>
                        </div>
                    </div>
                </div>
                
                <div class="main-content">
                    <div class="section">
                        <h2>Game-by-Game Stats</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Week</th>
                                    <th>Team</th>
                                    <th>Pass Yds</th>
                                    <th>Pass TDs</th>
                                    <th>Rush Yds</th>
                                    <th>Rush TDs</th>
                                    <th>Rec Yds</th>
                                    <th>Rec</th>
                                    <th>Rec TDs</th>
                                    <th>Sacks</th>
                                    <th>Tackles</th>
                                    <th>INTs</th>
                                    <th>FGM</th>
                                    <th>FGA</th>
                                    <th>Fantasy</th>
                                    <th>PPR</th>
                                    <th>Pass EPA</th>
                                    <th>Rush EPA</th>
                                    <th>Rec EPA</th>
                                </tr>
                            </thead>
                            <tbody>"""
        
        for i, stat in enumerate(stats, 1):
            html += f"""<tr>
                <td>{i}</td>
                <td>{getattr(stat, 'team', 'N/A')}</td>
                <td>{getattr(stat, 'passing_yards', 0) or 0}</td>
                <td>{getattr(stat, 'pass_tds', 0) or 0}</td>
                <td>{getattr(stat, 'rushing_yards', 0) or 0}</td>
                <td>{getattr(stat, 'rush_tds', 0) or 0}</td>
                <td>{getattr(stat, 'receiving_yards', 0) or 0}</td>
                <td>{getattr(stat, 'receptions', 0) or 0}</td>
                <td>{getattr(stat, 'rec_tds', 0) or 0}</td>
                <td>{getattr(stat, 'sacks', 0) or 0}</td>
                <td>{getattr(stat, 'tackles', 0) or 0}</td>
                <td>{getattr(stat, 'interceptions', 0) or 0}</td>
                <td>{getattr(stat, 'fgm', 0) or 0}</td>
                <td>{getattr(stat, 'fga', 0) or 0}</td>
                <td>{getattr(stat, 'fantasy_points', 0) or 0:.1f}</td>
                <td>{getattr(stat, 'fantasy_points_ppr', 0) or 0:.1f}</td>
                <td>{getattr(stat, 'passing_epa', 0) or 0:.2f}</td>
                <td>{getattr(stat, 'rushing_epa', 0) or 0:.2f}</td>
                <td>{getattr(stat, 'receiving_epa', 0) or 0:.2f}</td>
            </tr>"""
        
        html += """                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </body>
        </html>"""
        return html
    
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p><p>Player ID: {player_id}</p></body></html>"

if __name__ == "__main__":
    print("Starting Beautiful NFL Dashboard on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)