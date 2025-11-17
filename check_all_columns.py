#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import nflreadpy as nfl

# Load data and check all columns
df = nfl.load_player_stats(2023)
print("=== ALL AVAILABLE COLUMNS ===")
for i, col in enumerate(df.columns):
    print(f"{i+1:2d}. {col}")

# Check if there are any punting-specific stats
print("\n=== LOOKING FOR PUNTING DATA ===")
# Try to find punters with any non-zero stats
punters = df.filter(df['position'] == 'P')
print(f"Found {len(punters)} punter records")

# Check a few punters to see what data they have
sample_punter = punters.head(1)
if len(sample_punter) > 0:
    row = sample_punter.row(0, named=True)
    print(f"\nSample punter: {row.get('player_name')}")
    non_zero_stats = {}
    for col, val in row.items():
        if val is not None and val != 0 and val != "" and col not in ['player_id', 'player_name', 'player_display_name', 'position', 'position_group', 'headshot_url', 'season', 'week', 'season_type', 'team', 'opponent_team']:
            non_zero_stats[col] = val
    
    print("Non-zero stats:")
    for col, val in non_zero_stats.items():
        print(f"  {col}: {val}")