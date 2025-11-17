#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Check if database exists
db_path = "nfldb.db"
if not os.path.exists(db_path):
    print("Database does not exist!")
    exit(1)

# Connect and check schema
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== PLAYER TABLE SCHEMA ===")
cursor.execute("PRAGMA table_info(player)")
for row in cursor.fetchall():
    print(f"{row[1]} ({row[2]})")

print("\n=== PLAYERGAMESTAT TABLE SCHEMA ===")
cursor.execute("PRAGMA table_info(playergamestat)")
for row in cursor.fetchall():
    print(f"{row[1]} ({row[2]})")

print("\n=== SAMPLE DATA ===")
cursor.execute("SELECT * FROM playergamestat LIMIT 1")
row = cursor.fetchone()
if row:
    cursor.execute("PRAGMA table_info(playergamestat)")
    columns = [col[1] for col in cursor.fetchall()]
    for i, col in enumerate(columns):
        print(f"{col}: {row[i]}")
else:
    print("No data in playergamestat table")

conn.close()