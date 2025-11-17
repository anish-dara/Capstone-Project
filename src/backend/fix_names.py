import os
import sys
sys.path.append(os.path.dirname(__file__))

from database import get_engine, create_db_and_tables
from models import Player, PlayerGameStat
from crud import upsert_player
from sqlmodel import Session, select
import nflreadpy as nfl

def fix_missing_names():
    create_db_and_tables()
    engine = get_engine()
    
    # First, populate with roster data if empty
    with Session(engine) as session:
        player_count = session.exec(select(Player)).first()
        if not player_count:
            print("No players found, loading roster data...")
            df = nfl.load_rosters(2023)
            for row in df.iter_rows(named=True):
                player_id = str(row.get("gsis_id") or row.get("player_id") or row.get("nfl_id") or "")
                if player_id and player_id != "None":
                    p = Player(
                        player_id=player_id,
                        full_name=row.get("full_name"),
                        first_name=row.get("first_name"),
                        last_name=row.get("last_name"),
                        position=row.get("position"),
                    )
                    upsert_player(session, p)
    
    # Check for missing names
    with Session(engine) as session:
        players_no_name = session.exec(
            select(Player).where(
                (Player.full_name == None) | (Player.full_name == "")
            )
        ).all()
        
        print(f"Found {len(players_no_name)} players without names")
        
        for player in players_no_name:
            if player.first_name and player.last_name:
                player.full_name = f"{player.first_name} {player.last_name}"
                session.add(player)
        
        session.commit()
        print("Fixed names using first_name + last_name")

if __name__ == "__main__":
    fix_missing_names()