import nflreadpy as nfl
import polars as pl
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check what fields are available in the data
print("Loading 2023 player stats to check field names...")
df = nfl.load_player_stats(2023)

print("Available columns:")
print(df.columns)

print("\nChecking passing yards data:")
top_passers = df.filter(pl.col('passing_yards') > 0).sort('passing_yards', descending=True).head(10)
print("Top 10 single game passing performances:")
for row in top_passers.select(['player_display_name', 'week', 'passing_yards']).iter_rows(named=True):
    print(f"{row['player_display_name']}: Week {row['week']} - {row['passing_yards']} yards")

print("\nSeason totals (aggregated):")
season_totals = df.group_by('player_display_name').agg([
    pl.col('passing_yards').sum().alias('total_passing_yards'),
    pl.col('position').first()
]).filter(pl.col('total_passing_yards') > 1000).sort('total_passing_yards', descending=True).head(10)

for row in season_totals.iter_rows(named=True):
    print(f"{row['player_display_name']} ({row['position']}): {row['total_passing_yards']} yards")