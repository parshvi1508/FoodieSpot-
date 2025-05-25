from .database import session
from .models import Restaurant, Table

# Sample restaurants
restaurants_data = [
    {"name": "Spice Garden", "cuisine": "Indian", "location": "Downtown", "capacity": 40},
    {"name": "Pasta Palace", "cuisine": "Italian", "location": "Midtown", "capacity": 35},
    {"name": "Dragon Wok", "cuisine": "Chinese", "location": "Chinatown", "capacity": 50},
    {"name": "Le Bistro", "cuisine": "French", "location": "Uptown", "capacity": 30},
    {"name": "Taco Fiesta", "cuisine": "Mexican", "location": "Southside", "capacity": 45},
]

# Insert restaurants
for data in restaurants_data:
    restaurant = Restaurant(**data)
    session.add(restaurant)
    session.commit()
    
    # Add tables for each restaurant (different sizes)
    table_sizes = [2, 2, 4, 4, 4, 6, 6, 8, 10]
    for size in table_sizes:
        table = Table(restaurant_id=restaurant.id, capacity=size)
        session.add(table)

session.commit()
print("Sample data inserted successfully!")
