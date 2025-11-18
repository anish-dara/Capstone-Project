from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NFL Dashboard", "status": "running", "endpoints": ["/dashboard", "/players"]}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    # Sample NFL data for demo
    sample_leaders = [
        {"name": "Josh Allen", "team": "BUF", "stat": "4306", "pos": "QB"},
        {"name": "Tua Tagovailoa", "team": "MIA", "stat": "3548", "pos": "QB"},
        {"name": "Patrick Mahomes", "team": "KC", "stat": "4183", "pos": "QB"},
        {"name": "Lamar Jackson", "team": "BAL", "stat": "3678", "pos": "QB"},
        {"name": "Joe Burrow", "team": "CIN", "stat": "4475", "pos": "QB"}
    ]
    
    html = f"""
    <html>
    <head>
        <title>NFL Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .header {{ background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; }}
            .nav {{ display: flex; justify-content: space-between; align-items: center; }}
            .nav h1 {{ color: #2d3748; margin: 0; font-size: 2.5em; }}
            .nav-links a {{ background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-left: 10px; }}
            .main-content {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; }}
            td {{ padding: 14px 16px; border-bottom: 1px solid #e2e8f0; }}
            tr:nth-child(even) {{ background: #f7fafc; }}
            .rank {{ background: #667eea; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="nav">
                    <h1>🏈 NFL Dashboard</h1>
                    <div class="nav-links">
                        <a href="/dashboard">Stats</a>
                        <a href="/players">Players</a>
                    </div>
                </div>
            </div>
            <div class="main-content">
                <h2>Passing Yards Leaders (2023 Season)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Player</th>
                            <th>Position</th>
                            <th>Team</th>
                            <th>Passing Yards</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for i, leader in enumerate(sample_leaders, 1):
        html += f"""
        <tr>
            <td><div class="rank">{i}</div></td>
            <td><strong>{leader['name']}</strong></td>
            <td style="text-align: center;">{leader['pos']}</td>
            <td style="text-align: center;">{leader['team']}</td>
            <td style="text-align: center; font-weight: bold;">{leader['stat']}</td>
        </tr>
        """
    
    html += """
                    </tbody>
                </table>
                <p style="margin-top: 20px; color: #666;">Note: This is a demo version with sample data. Full database integration available in local version.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.get("/players", response_class=HTMLResponse)
def players():
    sample_players = [
        {"name": "Josh Allen", "pos": "QB"},
        {"name": "CeeDee Lamb", "pos": "WR"},
        {"name": "Christian McCaffrey", "pos": "RB"},
        {"name": "Travis Kelce", "pos": "TE"},
        {"name": "T.J. Watt", "pos": "LB"}
    ]
    
    html = """
    <html>
    <head>
        <title>NFL Players</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; }
            .nav { display: flex; justify-content: space-between; align-items: center; }
            .nav h1 { color: #2d3748; margin: 0; font-size: 2.5em; }
            .nav-links a { background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-left: 10px; }
            .main-content { background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }
            table { width: 100%; border-collapse: collapse; }
            th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; }
            td { padding: 14px 16px; border-bottom: 1px solid #e2e8f0; }
            tr:nth-child(even) { background: #f7fafc; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="nav">
                    <h1>👥 NFL Players</h1>
                    <div class="nav-links">
                        <a href="/dashboard">Stats</a>
                        <a href="/players">Players</a>
                    </div>
                </div>
            </div>
            <div class="main-content">
                <h2>Sample NFL Players</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Player</th>
                            <th>Position</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for player in sample_players:
        html += f"""
        <tr>
            <td><strong>{player['name']}</strong></td>
            <td style="text-align: center;">{player['pos']}</td>
        </tr>
        """
    
    html += """
                    </tbody>
                </table>
                <p style="margin-top: 20px; color: #666;">Note: This is a demo version with sample data. Full database integration available in local version.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

handler = app