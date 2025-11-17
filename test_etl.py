import sys
import os
sys.path.append('src')

from backend.database import create_db_and_tables, get_engine
from backend.etl import ingest_rosters, ingest_player_stats
from sqlmodel import Session, select
from backend.models import Player, PlayerGameStat

# Run ETL
create_db_and_tables()
ingest_rosters(2023)
ingest_player_stats([2023])

# Check results
engine = get_engine()
with Session(engine) as session:
    # Check player count
    player_count = len(session.exec(select(Player)).all())
    print(f"Players loaded: {player_count}")
    
    # Check stats count
    stats_count = len(session.exec(select(PlayerGameStat)).all())
    print(f"Stats loaded: {stats_count}")
    
    # Check top passers
    from sqlalchemy import func
    top_passers = session.exec(
        select(
            Player.full_name,
            func.sum(PlayerGameStat.passing_yards).label('total_yards')
        )
        .join(PlayerGameStat, Player.player_id == PlayerGameStat.player_id)
        .where(PlayerGameStat.passing_yards > 0)
        .group_by(Player.player_id, Player.full_name)
        .order_by(func.sum(PlayerGameStat.passing_yards).desc())
        .limit(5)
    ).all()
    
    print("\nTop 5 passers:")
    for passer in top_passers:
        print(f"{passer.full_name}: {passer.total_yards} yards")