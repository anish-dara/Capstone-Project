#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import nflreadpy as nfl

# Load sample data to see available columns
print("=== LOADING SAMPLE PLAYER STATS ===")
df = nfl.load_player_stats(2023)
print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns}")

# Check for kicking-related columns
kicking_cols = [col for col in df.columns if any(term in col.lower() for term in ['fg', 'kick', 'xp', 'pat'])]
print(f"\nKicking-related columns: {kicking_cols}")

# Sample some kicker data
print("\n=== SAMPLE KICKER DATA ===")
sample = df.filter(df['position'] == 'K').head(5)
if len(sample) > 0:
    for row in sample.iter_rows(named=True):
        print(f"Player: {row.get('player_name', 'Unknown')}")
        for col in kicking_cols:
            if col in row:
                print(f"  {col}: {row[col]}")
        print()
else:
    print("No kickers found in sample data")