#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Check punting stats in database
conn = sqlite3.connect("nfldb.db")
cursor = conn.cursor()

print("=== TOP PUNTERS BY TOTAL PUNTS ===")
cursor.execute("""
SELECT p.full_name, SUM(pgs.punts) as total_punts, AVG(pgs.avg_punt_distance) as avg_distance
FROM player p 
JOIN playergamestat pgs ON p.player_id = pgs.player_id 
WHERE p.position = 'P' AND pgs.season_type = 'REG' AND pgs.punts IS NOT NULL AND pgs.punts > 0
GROUP BY p.player_id, p.full_name
ORDER BY total_punts DESC
LIMIT 10
""")

for row in cursor.fetchall():
    name, punts, avg_dist = row
    print(f"{name}: {punts} punts, {avg_dist:.1f} avg yards")

print("\n=== SAMPLE PUNTING DATA ===")
cursor.execute("""
SELECT p.full_name, pgs.punts, pgs.avg_punt_distance, pgs.longest_punt, pgs.punts_inside_20, pgs.week
FROM player p 
JOIN playergamestat pgs ON p.player_id = pgs.player_id 
WHERE p.position = 'P' AND pgs.punts IS NOT NULL AND pgs.punts > 0
LIMIT 5
""")

for row in cursor.fetchall():
    print(f"{row[0]} - Week {row[5]}: {row[1]} punts, {row[2]} avg, {row[3]} long, {row[4]} inside 20")

conn.close()

# Check raw data for more stats
import nflreadpy as nfl
print("\n=== CHECKING RAW DATA FOR MORE STATS ===")
df = nfl.load_player_stats(2023)

# Look for punting columns
punt_cols = [col for col in df.columns if 'punt' in col.lower()]
print(f"Punting columns: {punt_cols}")

# Look for other interesting stats
other_cols = [col for col in df.columns if any(term in col.lower() for term in ['fumble', 'safety', 'return', 'penalty', 'epa', 'first_down'])]
print(f"Other interesting columns: {other_cols}")

# Sample punter data
print("\n=== SAMPLE PUNTER RAW DATA ===")
punters = df.filter(df['position'] == 'P').head(3)
for row in punters.iter_rows(named=True):
    print(f"Punter: {row.get('player_name')}")
    for col in punt_cols:
        if col in row and row[col] is not None:
            print(f"  {col}: {row[col]}")
    print()