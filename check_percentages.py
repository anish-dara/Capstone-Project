#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import nflreadpy as nfl

# Check percentage field ranges
df = nfl.load_player_stats(2023)

percentage_fields = ['fg_pct', 'pat_pct', 'target_share', 'air_yards_share', 'snap_pct']

print("=== PERCENTAGE FIELD RANGES ===")
for field in percentage_fields:
    if field in df.columns:
        min_val = df[field].min()
        max_val = df[field].max()
        print(f"{field}: {min_val} to {max_val}")
        
        # Sample some non-null values
        sample = df.filter(df[field].is_not_null()).head(3)
        print(f"  Sample values:")
        for row in sample.iter_rows(named=True):
            print(f"    {row.get('player_name')}: {row.get(field)}")
        print()
    else:
        print(f"{field}: Not found in data")
        print()