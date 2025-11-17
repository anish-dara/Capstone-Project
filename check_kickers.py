#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Connect to database
conn = sqlite3.connect("nfldb.db")
cursor = conn.cursor()

print("=== TOP KICKERS BY FIELD GOALS MADE ===")
cursor.execute("""
SELECT p.full_name, p.position, SUM(pgs.fgm) as total_fgm, SUM(pgs.fga) as total_fga
FROM player p 
JOIN playergamestat pgs ON p.player_id = pgs.player_id 
WHERE p.position = 'K' AND pgs.season_type = 'REG' AND pgs.fgm IS NOT NULL
GROUP BY p.player_id, p.full_name, p.position
ORDER BY total_fgm DESC
LIMIT 10
""")

for row in cursor.fetchall():
    name, pos, fgm, fga = row
    pct = (fgm / fga * 100) if fga > 0 else 0
    print(f"{name}: {fgm}/{fga} ({pct:.1f}%)")

print("\n=== SAMPLE KICKER DATA ===")
cursor.execute("""
SELECT p.full_name, pgs.fgm, pgs.fga, pgs.week, pgs.team
FROM player p 
JOIN playergamestat pgs ON p.player_id = pgs.player_id 
WHERE p.position = 'K' AND pgs.fgm IS NOT NULL AND pgs.fgm > 0
LIMIT 5
""")

for row in cursor.fetchall():
    print(f"{row[0]} - Week {row[3]} ({row[4]}): {row[1]} FGM, {row[2]} FGA")

conn.close()