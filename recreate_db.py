from sqlmodel import SQLModel, create_engine
from src.backend.models import Player, PlayerGameStat, Team, Season, Game

# Create engine (using the correct database file)
engine = create_engine("sqlite:///nfldb.db")

# Drop and recreate all tables
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

print("Database tables recreated successfully!")