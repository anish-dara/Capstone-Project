import nflreadpy as nfl

# Check what season types are available
df = nfl.load_player_stats(2023)
print("Available season_type values:")
print(df['season_type'].unique())

print("\nSample data with season_type:")
sample = df.select(['player_display_name', 'week', 'season_type', 'passing_yards']).head(10)
print(sample)