import requests
from typing import Dict, List, Optional
import time

BASE_URL = "http://localhost:5000"

class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.Timeout:
            print(f"⚠️ Request timeout for {endpoint}")
            raise
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Connection error for {endpoint}")
            raise
        except Exception as e:
            print(f"⚠️ Request error for {endpoint}: {e}")
            raise

# Global API client instance
api_client = APIClient()

# MISSING FUNCTIONS - ADD THESE FOR AI AGENT
def get_restaurants_ai() -> List[Dict]:
    """Get restaurants for AI agent"""
    try:
        response = api_client._make_request("GET", "/api/restaurants")
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('restaurants', [])
            print(f"✅ AI Retrieved {len(restaurants)} restaurants")
            return restaurants
        else:
            print(f"⚠️ Failed to get restaurants: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ AI Error fetching restaurants: {e}")
        return []

def check_availability_ai(restaurant_id: int, party_size: int, date: str, time: str) -> Dict:
    """Check availability for AI agent with validation"""
    try:
        # Input validation
        if not isinstance(restaurant_id, int) or restaurant_id <= 0:
            return {"available": False, "error": "Invalid restaurant ID"}
        if not isinstance(party_size, int) or not (1 <= party_size <= 20):
            return {"available": False, "error": "Party size must be between 1 and 20"}
        if not date or not isinstance(date, str):
            return {"available": False, "error": "Date is required"}
        if not time or not isinstance(time, str):
            return {"available": False, "error": "Time is required"}

        payload = {
            "restaurant_id": restaurant_id,
            "party_size": party_size,
            "date": date,
            "time": time
        }
        
        print(f"🔍 AI Checking availability: {payload}")
        response = api_client._make_request("POST", "/api/check_availability", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI Availability result: {result}")
            return result
        elif response.status_code == 400:
            try:
                error_data = response.json()
                return {"available": False, "error": error_data.get("error", "Bad request")}
            except:
                return {"available": False, "error": "Invalid request format"}
        else:
            return {"available": False, "error": f"Server error: {response.status_code}"}
            
    except Exception as e:
        print(f"❌ AI Error checking availability: {e}")
        return {"available": False, "error": str(e)}

def make_reservation_ai(user_name: str, user_phone: str, restaurant_id: int, 
                       table_id: int, party_size: int, date: str, time: str, 
                       user_email: str = "") -> Dict:
    """Make reservation for AI agent"""
    try:
        # Input validation
        if not user_name or len(user_name.strip()) < 2:
            return {"success": False, "error": "Valid name is required"}
        if not user_phone or len(user_phone.strip()) < 10:
            return {"success": False, "error": "Valid phone number is required"}

        payload = {
            "user_name": user_name.strip(),
            "user_phone": user_phone.strip(),
            "user_email": user_email.strip() if user_email else "",
            "restaurant_id": restaurant_id,
            "table_id": table_id,
            "party_size": party_size,
            "date": date,
            "time": time
        }
        
        print(f"🎯 AI Making reservation: {payload}")
        response = api_client._make_request("POST", "/api/make_reservation", json=payload)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ AI Reservation successful: {result}")
            return result
        elif response.status_code == 400:
            try:
                error_data = response.json()
                return {"success": False, "error": error_data.get("error", "Bad request")}
            except:
                return {"success": False, "error": "Invalid reservation request"}
        else:
            return {"success": False, "error": f"Server error: {response.status_code}"}
            
    except Exception as e:
        print(f"❌ AI Error making reservation: {e}")
        return {"success": False, "error": str(e)}

# UI FUNCTIONS (Keep existing for UI)
def get_restaurants() -> List[Dict]:
    """Get all restaurants with caching and error handling"""
    try:
        response = api_client._make_request("GET", "/api/restaurants")
        if response.status_code == 200:
            data = response.json()
            restaurants = data.get('restaurants', [])
            print(f"✅ Retrieved {len(restaurants)} restaurants")
            return restaurants
        else:
            print(f"⚠️ Failed to get restaurants: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching restaurants: {e}")
        return []

def check_availability(restaurant_id: int, party_size: int, date: str, time: str) -> Dict:
    """Check table availability with comprehensive validation"""
    try:
        # Input validation
        if not isinstance(restaurant_id, int) or restaurant_id <= 0:
            return {"available": False, "error": "Invalid restaurant ID"}
        if not isinstance(party_size, int) or not (1 <= party_size <= 20):
            return {"available": False, "error": "Party size must be between 1 and 20"}
        if not date or not isinstance(date, str):
            return {"available": False, "error": "Date is required"}
        if not time or not isinstance(time, str):
            return {"available": False, "error": "Time is required"}

        payload = {
            "restaurant_id": restaurant_id,
            "party_size": party_size,
            "date": date,
            "time": time
        }
        
        response = api_client._make_request("POST", "/api/check_availability", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result
        elif response.status_code == 400:
            try:
                error_data = response.json()
                return {"available": False, "error": error_data.get("error", "Bad request")}
            except:
                return {"available": False, "error": "Invalid request format"}
        else:
            return {"available": False, "error": f"Server error: {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"available": False, "error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"available": False, "error": "Unable to connect to server"}
    except Exception as e:
        return {"available": False, "error": f"Unexpected error: {str(e)}"}

def make_reservation(user_name: str, user_phone: str, restaurant_id: int,
                    table_id: int, party_size: int, date: str, time: str,
                    user_email: str = "") -> Dict:
    """Create a new reservation with validation"""
    try:
        # Input validation
        if not user_name or len(user_name.strip()) < 2:
            return {"success": False, "error": "Valid name is required (at least 2 characters)"}
        if not user_phone or len(user_phone.strip()) < 10:
            return {"success": False, "error": "Valid phone number is required (at least 10 digits)"}
        if not isinstance(restaurant_id, int) or restaurant_id <= 0:
            return {"success": False, "error": "Invalid restaurant ID"}
        if not isinstance(table_id, int) or table_id <= 0:
            return {"success": False, "error": "Invalid table ID"}
        if not isinstance(party_size, int) or not (1 <= party_size <= 20):
            return {"success": False, "error": "Party size must be between 1 and 20"}

        payload = {
            "user_name": user_name.strip(),
            "user_phone": user_phone.strip(),
            "user_email": user_email.strip() if user_email else "",
            "restaurant_id": restaurant_id,
            "table_id": table_id,
            "party_size": party_size,
            "date": date,
            "time": time
        }
        
        response = api_client._make_request("POST", "/api/make_reservation", json=payload)
        
        if response.status_code == 201:
            result = response.json()
            return result
        elif response.status_code == 400:
            try:
                error_data = response.json()
                return {"success": False, "error": error_data.get("error", "Bad request")}
            except:
                return {"success": False, "error": "Invalid reservation request"}
        else:
            return {"success": False, "error": f"Server error: {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def get_reservation(reservation_id: int) -> Optional[Dict]:
    """Get reservation details"""
    try:
        if not isinstance(reservation_id, int) or reservation_id <= 0:
            return None
        response = api_client._make_request("GET", f"/api/reservation/{reservation_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"❌ Error getting reservation: {e}")
        return None

def cancel_reservation(reservation_id: int) -> Dict:
    """Cancel reservation"""
    try:
        if not isinstance(reservation_id, int) or reservation_id <= 0:
            return {"success": False, "error": "Invalid reservation ID"}
        response = api_client._make_request("DELETE", f"/api/reservation/{reservation_id}")
        if response.status_code == 200:
            return {"success": True, "message": "Reservation cancelled successfully"}
        elif response.status_code == 404:
            return {"success": False, "error": "Reservation not found"}
        else:
            return {"success": False, "error": f"Failed to cancel reservation: {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def check_api_health() -> bool:
    """Check if the API is healthy and responsive"""
    try:
        response = api_client._make_request("GET", "/api/restaurants")
        return response.status_code == 200
    except:
        return False
