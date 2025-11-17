from fastapi import FastAPI, HTTPException
from typing import List
from sqlmodel import Session

from .database import create_db_and_tables, get_session
from .models import Player, Team
from .crud import get_players
from .etl import ingest_rosters, ingest_player_stats

app = FastAPI(title="NFL Sports DB Starter")


@app.on_event("startup")
def on_startup():
    # Create DB tables if they don't exist
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "NFL Sports DB API", "docs": "/docs"}


@app.get("/players", response_model=List[Player])
def list_players(limit: int = 100):
    with get_session() as session:
        return get_players(session, limit=limit)


@app.post("/etl")
def run_etl(season: int = 2023):
    """Run ETL pipeline to ingest NFL data for a given season."""
    try:
        ingest_rosters(season)
        ingest_player_stats([season])
        return {
            "status": "ok",
            "season": season,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )