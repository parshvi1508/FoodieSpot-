#!/usr/bin/env python3
"""
Update restaurant database with professional, realistic data
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from restaurant.sample_data import add_professional_restaurants, print_restaurant_statistics, reset_availability

def main():
    print("🏢 Updating Restaurant Database with Professional Data...")
    print("=" * 60)
    
    try:
        # Update restaurants with professional data
        add_professional_restaurants()
        
        print("\n" + "=" * 60)
        print("✅ Professional restaurant database update completed!")
        print("\nYour restaurant booking system now has:")
        print("• 40+ professional restaurants")
        print("• Diverse cuisine types and price ranges")
        print("• Realistic locations and capacities")
        print("• Professional table distributions")
        print("• Industry-standard restaurant types")
        
        # Offer to reset availability for testing
        reset_choice = input("\n🔄 Reset all table availability for fresh testing? (y/n): ")
        if reset_choice.lower() == 'y':
            reset_availability()
            print("✅ All tables reset to available for testing")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
