import os
from typing import List
from sqlmodel import Session
import nflreadpy as nfl
import polars as pl

from .database import get_engine, create_db_and_tables
from .models import Player, PlayerGameStat
from .crud import upsert_player, upsert_player_game_stat


def load_rosters(season: int):
    """Download rosters for a season using nflreadpy and return a data frame."""
    try:
        print(f"Downloading rosters for {season} via nflreadpy...")
        df = nfl.load_rosters(season)
        return df
    except Exception as e:
        print(f"Error loading rosters for {season}: {e}")
        raise


def ingest_rosters(season: int):
    df = load_rosters(season)
    engine = get_engine()
    
    with Session(engine) as session:
        count = 0
        for row in df.iter_rows(named=True):
            try:
                player_id = str(row.get("gsis_id") or row.get("player_id") or row.get("nfl_id") or "")
                
                if not player_id or player_id == "None":
                    continue
                
                first_name = row.get("first_name") or ""
                last_name = row.get("last_name") or ""
                full_name = row.get("full_name") or f"{first_name} {last_name}".strip()
                
                p = Player(
                    player_id=player_id,
                    full_name=full_name if full_name else None,
                    first_name=first_name if first_name else None,
                    last_name=last_name if last_name else None,
                    position=row.get("position"),
                )
                upsert_player(session, p)
                count += 1
            except Exception as e:
                print(f"Error processing player row: {e}")
                continue
        
        print(f"Processed {count} players for season {season}")


def ingest_player_stats(seasons: List[int]):
    engine = get_engine()
    
    for s in seasons:
        try:
            print(f"Loading player game stats for {s}...")
            df = nfl.load_player_stats(s)
            
            with Session(engine) as session:
                count = 0
                for row in df.iter_rows(named=True):
                    try:
                        player_id = str(row.get("player_id") or "")
                        
                        if not player_id or player_id == "None" or not row.get("week"):
                            continue
                        
                        def safe_float(val):
                            if val is None or val == "":
                                return None
                            try:
                                return float(val)
                            except (ValueError, TypeError):
                                return None
                        
                        def safe_int(val):
                            if val is None or val == "":
                                return None
                            try:
                                return int(val)
                            except (ValueError, TypeError):
                                return None
                        
                        stat = PlayerGameStat(
                            player_id=str(row.get("player_id")),
                            season=s,
                            week=safe_int(row.get("week")),
                            season_type=row.get("season_type", "REG"),
                            game_id=f"{s}_{row.get('week')}_{row.get('team')}",
                            team=row.get("team"),
                            snaps_played=safe_int(row.get("snaps")),
                            snap_percentage=safe_float(row.get("snap_pct")),
                            
                            # Passing stats
                            passing_yards=safe_float(row.get("passing_yards")),
                            completions=safe_int(row.get("completions")),
                            pass_attempts=safe_int(row.get("attempts")),
                            pass_interceptions=safe_int(row.get("interceptions")),
                            pass_tds=safe_int(row.get("passing_tds")),
                            qbr=safe_float(row.get("qbr")),
                            
                            # Rushing stats
                            rushing_yards=safe_float(row.get("rushing_yards")),
                            rush_attempts=safe_int(row.get("carries")),
                            rush_tds=safe_int(row.get("rushing_tds")),
                            
                            # Receiving stats
                            receiving_yards=safe_float(row.get("receiving_yards")),
                            receptions=safe_int(row.get("receptions")),
                            rec_targets=safe_int(row.get("targets")),
                            rec_tds=safe_int(row.get("receiving_tds")),
                            
                            # Offensive Line stats
                            sacks_allowed=safe_int(row.get("sacks_allowed")),
                            pressures_allowed=safe_int(row.get("pressures_allowed")),
                            
                            # Defensive stats
                            sacks=safe_float(row.get("def_sacks")),
                            qb_hits=safe_int(row.get("def_qb_hits")),
                            interceptions=safe_int(row.get("def_interceptions")),
                            tackles=safe_int((row.get("def_tackles_solo") or 0) + (row.get("def_tackles_with_assist") or 0)),
                            
                            # Kicker stats - FIXED MAPPING
                            fgm=safe_int(row.get("fg_made")),
                            fga=safe_int(row.get("fg_att")),
                            fg_percentage=safe_float(row.get("fg_pct")),
                            xpm=safe_int(row.get("pat_made")),
                            xpa=safe_int(row.get("pat_att")),
                            xp_percentage=safe_float(row.get("pat_pct")),
                            fg_50_plus_made=safe_int((row.get("fg_made_50_59") or 0) + (row.get("fg_made_60_") or 0)),
                            fg_50_plus_attempted=safe_int((row.get("fg_made_50_59") or 0) + (row.get("fg_missed_50_59") or 0) + (row.get("fg_made_60_") or 0) + (row.get("fg_missed_60_") or 0)),
                            
                            # Additional offensive stats
                            passing_first_downs=safe_int(row.get("passing_first_downs")),
                            passing_epa=safe_float(row.get("passing_epa")),
                            rushing_first_downs=safe_int(row.get("rushing_first_downs")),
                            rushing_epa=safe_float(row.get("rushing_epa")),
                            receiving_first_downs=safe_int(row.get("receiving_first_downs")),
                            receiving_epa=safe_float(row.get("receiving_epa")),
                            
                            # Fumble stats
                            rushing_fumbles=safe_int(row.get("rushing_fumbles")),
                            receiving_fumbles=safe_int(row.get("receiving_fumbles")),
                            def_fumbles_forced=safe_int(row.get("def_fumbles_forced")),
                            fumble_recovery_own=safe_int(row.get("fumble_recovery_own")),
                            fumble_recovery_opp=safe_int(row.get("fumble_recovery_opp")),
                            
                            # Return stats
                            punt_returns=safe_int(row.get("punt_returns")),
                            punt_return_yards=safe_float(row.get("punt_return_yards")),
                            kickoff_returns=safe_int(row.get("kickoff_returns")),
                            kickoff_return_yards=safe_float(row.get("kickoff_return_yards")),
                            
                            # Advanced defensive stats
                            def_tackles_for_loss=safe_int(row.get("def_tackles_for_loss")),
                            def_pass_defended=safe_int(row.get("def_pass_defended")),
                            def_safeties=safe_int(row.get("def_safeties")),
                            
                            # Special teams
                            special_teams_tds=safe_int(row.get("special_teams_tds")),
                            
                            # Penalties
                            penalties=safe_int(row.get("penalties")),
                            penalty_yards=safe_int(row.get("penalty_yards")),
                            
                            # Additional kicker stats
                            fg_long=safe_int(row.get("fg_long")),
                            gwfg_made=safe_int(row.get("gwfg_made")),
                            
                            # Additional defensive stats
                            def_interception_yards=safe_int(row.get("def_interception_yards")),
                            
                            # Fantasy points (for all players)
                            fantasy_points=safe_float(row.get("fantasy_points")),
                            fantasy_points_ppr=safe_float(row.get("fantasy_points_ppr")),
                            
                            # Advanced passing stats
                            passing_air_yards=safe_float(row.get("passing_air_yards")),
                            passing_yards_after_catch=safe_float(row.get("passing_yards_after_catch")),
                            passing_cpoe=safe_float(row.get("passing_cpoe")),
                            pacr=safe_float(row.get("pacr")),
                            
                            # Advanced receiving stats
                            receiving_air_yards=safe_float(row.get("receiving_air_yards")),
                            receiving_yards_after_catch=safe_float(row.get("receiving_yards_after_catch")),
                            racr=safe_float(row.get("racr")),
                            target_share=safe_float(row.get("target_share")),
                            air_yards_share=safe_float(row.get("air_yards_share")),
                            wopr=safe_float(row.get("wopr")),
                            
                            # Advanced rushing/receiving conversions
                            rushing_2pt_conversions=safe_int(row.get("rushing_2pt_conversions")),
                            passing_2pt_conversions=safe_int(row.get("passing_2pt_conversions")),
                            receiving_2pt_conversions=safe_int(row.get("receiving_2pt_conversions")),
                            
                            # Sack stats for QBs
                            sacks_suffered=safe_int(row.get("sacks_suffered")),
                            sack_yards_lost=safe_float(row.get("sack_yards_lost")),
                            sack_fumbles=safe_int(row.get("sack_fumbles")),
                            sack_fumbles_lost=safe_int(row.get("sack_fumbles_lost")),
                            
                            # Advanced defensive stats
                            def_sack_yards=safe_float(row.get("def_sack_yards")),
                            def_tackle_assists=safe_int(row.get("def_tackle_assists")),
                            def_tackles_for_loss_yards=safe_float(row.get("def_tackles_for_loss_yards")),
                            def_tds=safe_int(row.get("def_tds")),
                            
                            # Fumble recovery stats
                            fumble_recovery_yards_own=safe_float(row.get("fumble_recovery_yards_own")),
                            fumble_recovery_yards_opp=safe_float(row.get("fumble_recovery_yards_opp")),
                            fumble_recovery_tds=safe_int(row.get("fumble_recovery_tds")),
                            
                            # Miscellaneous
                            misc_yards=safe_float(row.get("misc_yards")),
                        )
                        upsert_player_game_stat(session, stat)
                        count += 1
                    except Exception as e:
                        print(f"Error processing stat row: {e}")
                        continue
                
                print(f"Processed {count} player stats for season {s}")
        except Exception as e:
            print(f"Error loading player stats for season {s}: {e}")
            continue


if __name__ == "__main__":
    try:
        create_db_and_tables()
        season = int(os.environ.get("SEASON", "2023"))
        print(f"Starting ETL process for season {season}")
        
        ingest_rosters(season)
        ingest_player_stats([season])
        
        print("ETL process completed successfully")
    except Exception as e:
        print(f"ETL process failed: {e}")
        raise