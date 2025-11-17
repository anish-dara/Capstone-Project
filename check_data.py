from sqlmodel import Session, select
from src.backend.database import get_engine
from src.backend.models import Player

engine = get_engine()
with Session(engine) as session:
    # Check total players
    total = session.exec(select(Player)).all()
    print(f"Total players: {len(total)}")
    
    # Check for Fred Warner specifically
    fred = session.exec(select(Player).where(Player.full_name.contains("Warner"))).all()
    print(f"Players with 'Warner': {len(fred)}")
    for p in fred:
        print(f"  - {p.full_name} ({p.position})")
    
    # Show first 5 players
    sample = session.exec(select(Player).limit(5)).all()
    print(f"\nFirst 5 players:")
    for p in sample:
        print(f"  - {p.full_name} ({p.position})")