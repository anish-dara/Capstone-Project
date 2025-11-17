from typing import Optional
from sqlmodel import SQLModel, Field


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: str = Field(index=True, unique=True)
    name: Optional[str]
    city: Optional[str]
    abbreviation: Optional[str]


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: str = Field(index=True, unique=True)
    full_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    position: Optional[str]
    birth_date: Optional[str]


class Season(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    year: int = Field(index=True, unique=True)


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: str = Field(index=True, unique=True)
    season: Optional[int]
    week: Optional[int]
    home_team: Optional[str]
    away_team: Optional[str]
    start_time: Optional[str]


class PlayerGameStat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: str = Field(index=True)
    season: int = Field(index=True)
    game_id: Optional[str] = Field(index=True)
    team: Optional[str]
    season_type: Optional[str] = Field(default="REG")
    passing_yards: Optional[float]
    rushing_yards: Optional[float]
    receiving_yards: Optional[float]
    attempts: Optional[int]
    receptions: Optional[int]
    pass_tds: Optional[int]
    rush_tds: Optional[int]
    rec_tds: Optional[int]
    sacks: Optional[float]
    tackles: Optional[int]
    interceptions: Optional[int]
    fgm: Optional[int]
    fga: Optional[int]
    fg_percentage: Optional[float]
    passing_epa: Optional[float]
    rushing_epa: Optional[float]
    receiving_epa: Optional[float]
    def_pass_defended: Optional[int]
    def_fumbles_forced: Optional[int]
    fantasy_points: Optional[float]
    fantasy_points_ppr: Optional[float]
    snaps_played: Optional[int]
    punt_returns: Optional[int]
    punt_return_yards: Optional[int]
    kickoff_returns: Optional[int]
    kickoff_return_yards: Optional[int]