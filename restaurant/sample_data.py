from .database import session
from .models import Restaurant, Table
import random

def add_professional_restaurants():
    """Add realistic, diverse restaurant data for professional booking system"""
    
    # PROFESSIONAL RESTAURANT DATABASE (Based on real restaurant industry data)
    professional_restaurants = [
        # FINE DINING & UPSCALE
        {"name": "The Metropolitan Grill", "cuisine": "Contemporary American", "location": "Downtown Financial", "capacity": 85, "price_range": "$$$$"},
        {"name": "Le Bernardin NYC", "cuisine": "French Seafood", "location": "Midtown West", "capacity": 62, "price_range": "$$$$"},
        {"name": "Eleven Madison Park", "cuisine": "Modern American", "location": "Flatiron District", "capacity": 78, "price_range": "$$$$"},
        {"name": "Per Se", "cuisine": "French Contemporary", "location": "Columbus Circle", "capacity": 64, "price_range": "$$$$"},
        {"name": "The Capital Grille", "cuisine": "American Steakhouse", "location": "Financial District", "capacity": 120, "price_range": "$$$"},
        
        # ITALIAN EXCELLENCE
        {"name": "Osteria Francescana", "cuisine": "Italian", "location": "Little Italy", "capacity": 45, "price_range": "$$$"},
        {"name": "Villa Crespi", "cuisine": "Northern Italian", "location": "Upper East Side", "capacity": 38, "price_range": "$$$"},
        {"name": "Pasta Palace", "cuisine": "Italian", "location": "Midtown", "capacity": 65, "price_range": "$$"},
        {"name": "Nonna's Kitchen", "cuisine": "Traditional Italian", "location": "Brooklyn Heights", "capacity": 52, "price_range": "$$"},
        {"name": "Il Mulino", "cuisine": "Italian", "location": "Greenwich Village", "capacity": 70, "price_range": "$$$"},
        
        # ASIAN CUISINE SPECIALISTS
        {"name": "Spice Garden", "cuisine": "Indian", "location": "Curry Hill", "capacity": 80, "price_range": "$$"},
        {"name": "Bukhara", "cuisine": "North Indian", "location": "Jackson Heights", "capacity": 95, "price_range": "$$"},
        {"name": "Indian Accent", "cuisine": "Modern Indian", "location": "Midtown East", "capacity": 55, "price_range": "$$$"},
        {"name": "Dragon Palace", "cuisine": "Chinese", "location": "Chinatown", "capacity": 110, "price_range": "$$"},
        {"name": "Nobu", "cuisine": "Japanese", "location": "Tribeca", "capacity": 85, "price_range": "$$$$"},
        {"name": "Sushi Yasuda", "cuisine": "Japanese Sushi", "location": "Midtown East", "capacity": 45, "price_range": "$$$"},
        {"name": "Din Tai Fung", "cuisine": "Taiwanese", "location": "Upper West Side", "capacity": 90, "price_range": "$$"},
        
        # TRENDY & CONTEMPORARY
        {"name": "The Standard Grill", "cuisine": "Contemporary American", "location": "Meatpacking District", "capacity": 75, "price_range": "$$$"},
        {"name": "Beauty & Essex", "cuisine": "Global Fusion", "location": "Lower East Side", "capacity": 140, "price_range": "$$$"},
        {"name": "ABC Kitchen", "cuisine": "Farm-to-Table", "location": "Union Square", "capacity": 85, "price_range": "$$$"},
        {"name": "The Spotted Pig", "cuisine": "British Gastropub", "location": "West Village", "capacity": 60, "price_range": "$$"},
        {"name": "Momofuku Noodle Bar", "cuisine": "Asian Fusion", "location": "East Village", "capacity": 70, "price_range": "$$"},
        
        # SEAFOOD SPECIALISTS
        {"name": "Grand Central Oyster Bar", "cuisine": "Seafood", "location": "Midtown East", "capacity": 150, "price_range": "$$$"},
        {"name": "The Ocean House", "cuisine": "Coastal Seafood", "location": "Chelsea", "capacity": 95, "price_range": "$$$"},
        {"name": "Luke's Lobster", "cuisine": "Casual Seafood", "location": "Multiple Locations", "capacity": 35, "price_range": "$"},
        
        # STEAKHOUSES & GRILLS
        {"name": "Peter Luger Steak House", "cuisine": "Steakhouse", "location": "Williamsburg", "capacity": 90, "price_range": "$$$$"},
        {"name": "Wolfgang's Steakhouse", "cuisine": "Prime Steaks", "location": "Midtown", "capacity": 110, "price_range": "$$$$"},
        {"name": "The Grill", "cuisine": "American Grill", "location": "Midtown", "capacity": 120, "price_range": "$$$"},
        
        # INTERNATIONAL FLAVORS
        {"name": "Casa Mono", "cuisine": "Spanish Tapas", "location": "Gramercy", "capacity": 65, "price_range": "$$$"},
        {"name": "Le Bernardin", "cuisine": "French", "location": "Midtown West", "capacity": 62, "price_range": "$$$$"},
        {"name": "Frenchette", "cuisine": "French Bistro", "location": "Tribeca", "capacity": 80, "price_range": "$$$"},
        {"name": "Cote", "cuisine": "Korean BBQ", "location": "Flatiron", "capacity": 85, "price_range": "$$$"},
        {"name": "Pujol", "cuisine": "Modern Mexican", "location": "SoHo", "capacity": 70, "price_range": "$$$"},
        
        # CASUAL DINING & COMFORT FOOD
        {"name": "Shake Shack", "cuisine": "American Burgers", "location": "Multiple Locations", "capacity": 60, "price_range": "$"},
        {"name": "Joe's Pizza", "cuisine": "New York Pizza", "location": "Multiple Locations", "capacity": 40, "price_range": "$"},
        {"name": "Katz's Delicatessen", "cuisine": "Jewish Deli", "location": "Lower East Side", "capacity": 100, "price_range": "$$"},
        {"name": "Russ & Daughters", "cuisine": "Jewish Appetizing", "location": "Lower East Side", "capacity": 50, "price_range": "$$"},
        {"name": "Clinton St. Baking Co.", "cuisine": "American Brunch", "location": "Lower East Side", "capacity": 45, "price_range": "$$"},
        
        # ROOFTOP & SPECIAL VENUES
        {"name": "230 Fifth Rooftop", "cuisine": "American Contemporary", "location": "Flatiron Rooftop", "capacity": 200, "price_range": "$$$"},
        {"name": "The Press Lounge", "cuisine": "Contemporary", "location": "Hell's Kitchen Rooftop", "capacity": 180, "price_range": "$$$"},
        {"name": "Rainbow Room", "cuisine": "Contemporary American", "location": "Rockefeller Center", "capacity": 150, "price_range": "$$$$"},
        
        # HEALTHY & ORGANIC
        {"name": "Candle Cafe", "cuisine": "Organic Vegan", "location": "Upper East Side", "capacity": 55, "price_range": "$$"},
        {"name": "Pure Food and Wine", "cuisine": "Raw Vegan", "location": "Gramercy", "capacity": 65, "price_range": "$$$"},
        {"name": "Sweetgreen", "cuisine": "Healthy Salads", "location": "Multiple Locations", "capacity": 45, "price_range": "$"},
        
        # BRUNCH SPECIALISTS
        {"name": "Sarabeth's", "cuisine": "American Brunch", "location": "Upper East Side", "capacity": 75, "price_range": "$$"},
        {"name": "Bubby's", "cuisine": "American Comfort", "location": "Tribeca", "capacity": 85, "price_range": "$$"},
        {"name": "The Smith", "cuisine": "American Brasserie", "location": "Multiple Locations", "capacity": 120, "price_range": "$$"},
        
        # DESSERT & SPECIALTY
        {"name": "Serendipity 3", "cuisine": "Desserts & American", "location": "Upper East Side", "capacity": 90, "price_range": "$$"},
        {"name": "Lady M Cake Boutique", "cuisine": "French Pastries", "location": "Multiple Locations", "capacity": 25, "price_range": "$$"},
    ]
    
    print(f"[DEBUG] Processing {len(professional_restaurants)} professional restaurants...")
    
    # Clear existing data
    try:
        session.query(Table).delete()
        session.query(Restaurant).delete()
        session.commit()
        print("[DEBUG] Cleared existing restaurant data")
    except Exception as e:
        print(f"[DEBUG] Error clearing data: {e}")
        session.rollback()
    
    # Add professional restaurants
    added_count = 0
    for restaurant_data in professional_restaurants:
        try:
            # Check if restaurant already exists
            existing = session.query(Restaurant).filter_by(name=restaurant_data['name']).first()
            if existing:
                print(f"[DEBUG] Skipping duplicate: {restaurant_data['name']}")
                continue
            
            # Create restaurant
            restaurant = Restaurant(
                name=restaurant_data['name'],
                cuisine=restaurant_data['cuisine'],
                location=restaurant_data['location'],
                capacity=restaurant_data['capacity']
            )
            session.add(restaurant)
            session.flush()  # Get the ID
            
            # Add realistic table distribution
            tables_added = add_professional_tables(restaurant, restaurant_data.get('price_range', '$$'))
            
            added_count += 1
            print(f"[DEBUG] ✅ Added: {restaurant.name} ({restaurant.cuisine}) - {tables_added} tables")
            
        except Exception as e:
            print(f"[DEBUG] ❌ Error adding {restaurant_data['name']}: {e}")
            session.rollback()
            continue
    
    # Commit all changes
    try:
        session.commit()
        print(f"[DEBUG] 🎉 Successfully added {added_count} professional restaurants!")
        print_restaurant_statistics()
    except Exception as e:
        print(f"[DEBUG] ❌ Error committing: {e}")
        session.rollback()

def add_professional_tables(restaurant, price_range):
    """Add realistic table distribution based on restaurant type and price range"""
    capacity = restaurant.capacity
    tables_added = 0
    
    # Table distribution based on restaurant type and price range
    if price_range == "$$$$":  # Fine dining
        # Fine dining has more intimate seating
        if capacity <= 60:
            table_sizes = [2, 2, 2, 4, 4, 6, 8]  # More 2-tops for intimate dining
        else:
            table_sizes = [2, 2, 2, 2, 4, 4, 4, 6, 6, 8, 10]
    elif price_range == "$$$":  # Upscale casual
        # Mix of table sizes for groups
        if capacity <= 80:
            table_sizes = [2, 2, 4, 4, 4, 6, 6, 8]
        else:
            table_sizes = [2, 2, 2, 4, 4, 4, 4, 6, 6, 6, 8, 10]
    elif price_range == "$$":  # Casual dining
        # More family-friendly sizes
        if capacity <= 60:
            table_sizes = [2, 4, 4, 4, 6, 6, 8]
        elif capacity <= 100:
            table_sizes = [2, 2, 4, 4, 4, 4, 6, 6, 6, 8, 8, 10]
        else:
            table_sizes = [2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 8, 8, 10, 12]
    else:  # $ - Fast casual/quick service
        # Smaller, efficient seating
        table_sizes = [2, 2, 4, 4, 4, 6, 6]
    
    # Add tables ensuring we don't exceed capacity
    total_seats = 0
    table_number = 1
    
    for size in table_sizes:
        if total_seats + size <= capacity:
            table = Table(
                restaurant_id=restaurant.id,
                capacity=size,
                is_available=True
            )
            session.add(table)
            total_seats += size
            tables_added += 1
            table_number += 1
        else:
            break
    
    # Add remaining capacity with appropriate table sizes
    remaining_capacity = capacity - total_seats
    while remaining_capacity >= 2:
        if remaining_capacity >= 6:
            size = 6
        elif remaining_capacity >= 4:
            size = 4
        else:
            size = 2
            
        table = Table(
            restaurant_id=restaurant.id,
            capacity=size,
            is_available=True
        )
        session.add(table)
        total_seats += size
        tables_added += 1
        remaining_capacity -= size
    
    return tables_added

def print_restaurant_statistics():
    """Print comprehensive restaurant statistics"""
    try:
        total_restaurants = session.query(Restaurant).count()
        cuisines = session.query(Restaurant.cuisine).distinct().all()
        locations = session.query(Restaurant.location).distinct().all()
        
        print(f"\n📊 Professional Restaurant Database Statistics:")
        print(f"Total Restaurants: {total_restaurants}")
        print(f"Unique Cuisines: {len(cuisines)}")
        print(f"Unique Locations: {len(locations)}")
        
        # Cuisine distribution
        print(f"\n🍽️ Cuisine Distribution:")
        cuisine_counts = {}
        for restaurant in session.query(Restaurant).all():
            cuisine = restaurant.cuisine
            cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
        
        for cuisine, count in sorted(cuisine_counts.items()):
            print(f"  {cuisine}: {count} restaurants")
        
        # Location distribution
        print(f"\n📍 Location Distribution:")
        location_counts = {}
        for restaurant in session.query(Restaurant).all():
            location = restaurant.location
            location_counts[location] = location_counts.get(location, 0) + 1
        
        for location, count in sorted(location_counts.items()):
            print(f"  {location}: {count} restaurants")
        
        # Capacity analysis
        total_capacity = sum(r.capacity for r in session.query(Restaurant).all())
        avg_capacity = total_capacity / total_restaurants if total_restaurants > 0 else 0
        print(f"\n👥 Capacity Analysis:")
        print(f"  Total System Capacity: {total_capacity} seats")
        print(f"  Average Restaurant Size: {avg_capacity:.1f} seats")
        
        # Table statistics
        total_tables = session.query(Table).count()
        available_tables = session.query(Table).filter_by(is_available=True).count()
        print(f"\n🪑 Table Statistics:")
        print(f"  Total Tables: {total_tables}")
        print(f"  Available Tables: {available_tables}")
        
    except Exception as e:
        print(f"[DEBUG] Error getting statistics: {e}")

def reset_availability():
    """Reset all tables to available (useful for testing)"""
    try:
        session.query(Table).update({"is_available": True})
        session.commit()
        print("[DEBUG] ✅ All tables reset to available")
    except Exception as e:
        print(f"[DEBUG] ❌ Error resetting availability: {e}")
        session.rollback()

if __name__ == "__main__":
    print("[DEBUG] Starting professional restaurant data population...")
    add_professional_restaurants()
    print("[DEBUG] Professional restaurant data population complete!")
