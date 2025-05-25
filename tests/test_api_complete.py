import requests
import json
import pytest
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

class TestFoodieSpotAPI:
    
    def test_api_root(self):
        """Test the root endpoint"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        print("✅ Root endpoint test passed")

    def test_get_restaurants(self):
        """Test GET /api/restaurants"""
        response = requests.get(f"{BASE_URL}/api/restaurants")
        assert response.status_code == 200
        data = response.json()
        assert "restaurants" in data
        assert len(data["restaurants"]) > 0
        
        # Check restaurant structure
        restaurant = data["restaurants"][0]
        required_fields = ["id", "name", "cuisine", "location", "capacity"]
        for field in required_fields:
            assert field in restaurant
        
        print(f"✅ Found {len(data['restaurants'])} restaurants")
        return data["restaurants"]

    def test_get_users(self):
        """Test GET /api/users"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        print(f"✅ Users endpoint working - {len(data['users'])} users found")

    def test_check_availability(self):
        """Test POST /api/check_availability"""
        # Get a restaurant first
        restaurants = requests.get(f"{BASE_URL}/api/restaurants").json()["restaurants"]
        restaurant_id = restaurants[0]["id"]
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        payload = {
            "restaurant_id": restaurant_id,
            "party_size": 4,
            "date": tomorrow,
            "time": "19:00"
        }
        
        response = requests.post(f"{BASE_URL}/api/check_availability", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "available" in data
        print(f"✅ Availability check: {data}")

    def test_make_reservation(self):
        """Test POST /api/make_reservation"""
        # First check availability
        restaurants = requests.get(f"{BASE_URL}/api/restaurants").json()["restaurants"]
        restaurant_id = restaurants[0]["id"]
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        availability_payload = {
            "restaurant_id": restaurant_id,
            "party_size": 2,
            "date": tomorrow,
            "time": "20:00"
        }
        
        availability_response = requests.post(
            f"{BASE_URL}/api/check_availability", 
            json=availability_payload
        )
        
        if availability_response.json().get("available"):
            table_id = availability_response.json().get("suggested_table_id")
            
            reservation_payload = {
                "user_name": "Test User",
                "user_phone": "9999999999",
                "user_email": "test@example.com",
                "restaurant_id": restaurant_id,
                "table_id": table_id,
                "party_size": 2,
                "date": tomorrow,
                "time": "20:00"
            }
            
            response = requests.post(f"{BASE_URL}/api/make_reservation", json=reservation_payload)
            assert response.status_code == 201
            data = response.json()
            assert data["success"] == True
            assert "reservation_id" in data
            print(f"✅ Reservation created: ID {data['reservation_id']}")
            
            # Test getting the reservation
            reservation_id = data["reservation_id"]
            get_response = requests.get(f"{BASE_URL}/api/reservation/{reservation_id}")
            assert get_response.status_code == 200
            reservation_data = get_response.json()
            assert reservation_data["user_name"] == "Test User"
            print(f"✅ Reservation retrieval successful")
            
        else:
            print("⚠️ No tables available for reservation test")

    def test_error_handling(self):
        """Test error handling"""
        # Test invalid availability check
        invalid_payload = {
            "restaurant_id": 999,  # Non-existent restaurant
            "party_size": 4,
            "date": "2025-05-26",
            "time": "19:00"
        }
        
        response = requests.post(f"{BASE_URL}/api/check_availability", json=invalid_payload)
        # Should handle gracefully (might return available=False or error)
        assert response.status_code in [200, 400]
        print("✅ Error handling test passed")

def run_all_tests():
    """Run all tests in sequence"""
    tester = TestFoodieSpotAPI()
    
    print("🚀 Starting FoodieSpot API Tests...")
    print("-" * 50)
    
    try:
        tester.test_api_root()
        tester.test_get_restaurants()
        tester.test_get_users()
        tester.test_check_availability()
        tester.test_make_reservation()
        tester.test_error_handling()
        
        print("-" * 50)
        print("🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_all_tests()
