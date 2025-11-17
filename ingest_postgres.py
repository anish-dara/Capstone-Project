import os
from typing import Optional
import nflreadpy as nfl
from sqlmodel import SQLModel, Field, create_engine, Session

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: str = Field(index=True)
    full_name: Optional[str]
    position: Optional[str]

class PlayerGameStat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: str = Field(index=True)
    season: int
    game_id: Optional[str]
    team: Optional[str]
    passing_yards: Optional[float]
    rushing_yards: Optional[float]
    receiving_yards: Optional[float]

def main():
    database_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/nfldb")
    engine = create_engine(database_url)
    print("Connecting to:", database_url)
    SQLModel.metadata.create_all(engine)
    season = int(os.environ.get("SEASON", "2023"))

    print(f"Downloading rosters for {season}...")
    rosters = nfl.load_rosters(season)
    print(f"Downloaded {len(rosters)} roster rows")

    with Session(engine) as session:
        inserted = 0
        for row in rosters.iter_rows(named=True):
            pid = str(row.get("gsis_id") or row.get("player_id") or row.get("nfl_id") or "unknown")
            p = Player(player_id=pid, full_name=row.get("full_name") or "", position=row.get("position"))
            try:
                session.add(p)
                inserted += 1
            except Exception:
                session.rollback()
        session.commit()
    print(f"Inserted ~{inserted} players into Postgres")

    print(f"Downloading player game stats for {season}...")
    stats = nfl.load_player_stats(season)
    print(f"Downloaded {len(stats)} player-game stat rows")

    with Session(engine) as session:
        count = 0
        for row in stats.iter_rows(named=True):
            if count >= 1000:  # limit for initial ingestion
                break
            pid = str(row.get("player_id") or row.get("gsis_id") or "unknown")
            stat = PlayerGameStat(
                player_id=pid,
                season=season,
                game_id=row.get("game_id"),
                team=row.get("team"),
                passing_yards=row.get("pass_yds"),
                rushing_yards=row.get("rush_yds"),
                receiving_yards=row.get("rec_yds"),
            )
            session.add(stat)
            count += 1
        session.commit()
    print(f"Inserted {count} player-game stat rows into Postgres")

    with Session(engine) as session:
        total_players = session.query(Player).count()
        total_stats = session.query(PlayerGameStat).count()
    print(f"Postgres totals: players={total_players}, stats={total_stats}")

if __name__ == "__main__":
    main()
