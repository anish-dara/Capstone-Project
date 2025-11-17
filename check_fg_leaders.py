#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import nflreadpy as nfl

# Load 2023 data and find FG leaders
print("=== TOP FIELD GOAL LEADERS (2023 Regular Season) ===")
df = nfl.load_player_stats(2023)

# Filter for kickers in regular season with FG data
kickers = df.filter(
    (df['position'] == 'K') & 
    (df['season_type'] == 'REG') & 
    (df['fg_made'].is_not_null())
)

# Group by player and sum FG stats
import polars as pl
fg_leaders = kickers.group_by(['player_id', 'player_name']).agg([
    pl.col('fg_made').sum().alias('total_fg_made'),
    pl.col('fg_att').sum().alias('total_fg_att')
]).sort('total_fg_made', descending=True)

print("Top 10 Kickers by Field Goals Made:")
for row in fg_leaders.head(10).iter_rows(named=True):
    name = row['player_name']
    made = row['total_fg_made']
    att = row['total_fg_att']
    pct = (made / att * 100) if att > 0 else 0
    print(f"{name}: {made}/{att} ({pct:.1f}%)")