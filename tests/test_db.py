from restaurant.database import session
from restaurant.models import Restaurant, Table

# Test: List all restaurants
restaurants = session.query(Restaurant).all()
for r in restaurants:
    print(f"{r.name} - {r.cuisine} - {r.location}")
    tables = session.query(Table).filter_by(restaurant_id=r.id).all()
    print(f"  Tables: {len(tables)} (capacities: {[t.capacity for t in tables]})")
