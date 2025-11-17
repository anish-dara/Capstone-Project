#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Check CPOE values in database
conn = sqlite3.connect("nfldb.db")
cursor = conn.cursor()

print("=== CPOE VALUES FOR QBs ===")
cursor.execute("""
SELECT p.full_name, pgs.passing_cpoe, pgs.week, pgs.completions, pgs.pass_attempts
FROM player p 
JOIN playergamestat pgs ON p.player_id = pgs.player_id 
WHERE p.position = 'QB' AND pgs.season_type = 'REG' AND pgs.passing_cpoe IS NOT NULL
ORDER BY pgs.passing_cpoe DESC
LIMIT 10
""")

for row in cursor.fetchall():
    name, cpoe, week, comp, att = row
    print(f"{name} - Week {week}: CPOE={cpoe}, {comp}/{att}")

conn.close()

# Check raw data CPOE values
import nflreadpy as nfl
print("\n=== RAW DATA CPOE VALUES ===")
df = nfl.load_player_stats(2023)

# Sample QB CPOE data
qbs = df.filter((df['position'] == 'QB') & (df['passing_cpoe'].is_not_null())).head(5)
for row in qbs.iter_rows(named=True):
    name = row.get('player_name')
    cpoe = row.get('passing_cpoe')
    comp = row.get('completions')
    att = row.get('attempts')
    print(f"{name}: CPOE={cpoe}, {comp}/{att}")

print(f"\nCPOE range in data: {df['passing_cpoe'].min()} to {df['passing_cpoe'].max()}")