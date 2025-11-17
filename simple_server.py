from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <head><title>NFL Dashboard</title></head>
    <body style="font-family: Arial; margin: 40px;">
    <h1>NFL Dashboard</h1>
    <p>Dashboard is running successfully!</p>
    <table border="1">
    <tr><th>Player</th><th>Team</th><th>Stats</th></tr>
    <tr><td>CeeDee Lamb</td><td>DAL</td><td>135 Receptions</td></tr>
    <tr><td>T.J. Watt</td><td>PIT</td><td>19.0 Sacks</td></tr>
    </table>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)