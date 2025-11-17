#!/usr/bin/env python
import nflreadpy as nfl
from sqlmodel import Session
from src.backend.database import create_db_and_tables, get_engine
from src.backend.models import Player, PlayerGameStat

def main():
    print("=" * 60)
    print("NFL Sports DB - Demo Ingestion")
    print("=" * 60)
    
    print("\n1. Creating database tables...")
    create_db_and_tables()
    print("    Tables created")
    
    print("\n2. Downloading 2023 NFL rosters via nflreadpy...")
    rosters_df = nfl.load_rosters(2023)
    print(f"    Downloaded {len(rosters_df)} roster entries")
    
    print("\n3. Inserting rosters into database...")
    engine = get_engine()
    with Session(engine) as session:
        for row in rosters_df.iter_rows(named=True):
            player_id = str(row.get("gsis_id") or row.get("player_id") or "unknown")
            player = Player(
                player_id=player_id,
                full_name=row.get("full_name") or f"{row.get('first_name', '')} {row.get('last_name', '')}".strip(),
                first_name=row.get("first_name"),
                last_name=row.get("last_name"),
                position=row.get("position"),
            )
            session.add(player)
        session.commit()
    print(f"    Inserted {len(rosters_df)} players")
    
    print("\n4. Downloading 2023 player game stats via nflreadpy...")
    stats_df = nfl.load_player_stats(2023)
    print(f"    Downloaded {len(stats_df)} player-game stat rows")
    
    print("\n5. Inserting player stats into database (first 100 for demo)...")
    with Session(engine) as session:
        count = 0
        for row in stats_df.iter_rows(named=True):
            if count >= 100:
                break
            player_id = str(row.get("player_id") or row.get("gsis_id") or "unknown")
            stat = PlayerGameStat(
                player_id=player_id,
                season=2023,
                game_id=row.get("game_id"),
                team=row.get("team"),
                passing_yards=row.get("pass_yds"),
                rushing_yards=row.get("rush_yds"),
                receiving_yards=row.get("rec_yds"),
                attempts=row.get("pass_att") or row.get("rush_att"),
                receptions=row.get("rec"),
            )
            session.add(stat)
            count += 1
        session.commit()
    print(f"    Inserted {count} player game stats")
    
    print("\n6. Querying database...")
    with Session(engine) as session:
        total_players = session.query(Player).count()
        total_stats = session.query(PlayerGameStat).count()
        sample_players = session.query(Player).limit(3).all()
    
    print(f"   Total players in DB: {total_players}")
    print(f"   Total player-game stats in DB: {total_stats}")
    print(f"\n   Sample players:")
    for p in sample_players:
        print(f"     - {p.full_name} ({p.position})")
    
    print("\n" + "=" * 60)
    print(" Demo complete! Data stored in nfldb.db")
    print("=" * 60)

if __name__ == "__main__":
    main()
