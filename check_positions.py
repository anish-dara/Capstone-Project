#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Connect to database
conn = sqlite3.connect("nfldb.db")
cursor = conn.cursor()

print("=== POSITIONS IN DATABASE ===")
cursor.execute("SELECT position, COUNT(*) FROM player WHERE position IS NOT NULL GROUP BY position ORDER BY COUNT(*) DESC")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} players")

print("\n=== PLAYERS WITH STATS BY POSITION ===")
cursor.execute("""
SELECT p.position, COUNT(DISTINCT p.player_id) 
FROM player p 
JOIN playergamestat pgs ON p.player_id = pgs.player_id 
WHERE p.position IS NOT NULL 
GROUP BY p.position 
ORDER BY COUNT(DISTINCT p.player_id) DESC
""")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} players with stats")

conn.close()