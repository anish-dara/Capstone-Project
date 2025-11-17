import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Get table schema
cursor.execute("PRAGMA table_info(player)")
columns = cursor.fetchall()

print("Player table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()