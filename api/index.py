from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "NFL Dashboard API", "status": "running"}
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>NFL Dashboard</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                    .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                    .header { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; }
                    .nav { display: flex; justify-content: space-between; align-items: center; }
                    .nav h1 { color: #2d3748; margin: 0; }
                    .nav-links a { background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-left: 10px; }
                    .main-content { background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }
                    table { width: 100%; border-collapse: collapse; }
                    th { background: #667eea; color: white; padding: 16px; }
                    td { padding: 14px 16px; border-bottom: 1px solid #e2e8f0; }
                    tr:nth-child(even) { background: #f7fafc; }
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
                        <h2>NFL Passing Yards Leaders</h2>
                        <table>
                            <tr><th>Rank</th><th>Player</th><th>Team</th><th>Yards</th></tr>
                            <tr><td>1</td><td>Josh Allen</td><td>BUF</td><td>4306</td></tr>
                            <tr><td>2</td><td>Tua Tagovailoa</td><td>MIA</td><td>3548</td></tr>
                            <tr><td>3</td><td>Patrick Mahomes</td><td>KC</td><td>4183</td></tr>
                            <tr><td>4</td><td>Lamar Jackson</td><td>BAL</td><td>3678</td></tr>
                            <tr><td>5</td><td>Joe Burrow</td><td>CIN</td><td>4475</td></tr>
                        </table>
                        <p style="color: #666; margin-top: 20px;">Demo version with sample NFL data</p>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/players':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head>
                <title>NFL Players</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                    .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                    .header { background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 30px; }
                    .nav { display: flex; justify-content: space-between; align-items: center; }
                    .nav h1 { color: #2d3748; margin: 0; }
                    .nav-links a { background: #4299e1; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-left: 10px; }
                    .main-content { background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }
                    table { width: 100%; border-collapse: collapse; }
                    th { background: #667eea; color: white; padding: 16px; }
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
                            <tr><th>Player</th><th>Position</th></tr>
                            <tr><td>Josh Allen</td><td>QB</td></tr>
                            <tr><td>CeeDee Lamb</td><td>WR</td></tr>
                            <tr><td>Christian McCaffrey</td><td>RB</td></tr>
                            <tr><td>Travis Kelce</td><td>TE</td></tr>
                            <tr><td>T.J. Watt</td><td>LB</td></tr>
                        </table>
                        <p style="color: #666; margin-top: 20px;">Demo version with sample NFL data</p>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1>')