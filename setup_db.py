#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.database import create_db_and_tables
from backend.etl import ingest_rosters, ingest_player_stats

if __name__ == "__main__":
    print("Creating database tables...")
    create_db_and_tables()
    
    print("Loading 2023 rosters...")
    ingest_rosters(2023)
    
    print("Loading 2023 player stats...")
    ingest_player_stats([2023])
    
    print("Database setup complete!")