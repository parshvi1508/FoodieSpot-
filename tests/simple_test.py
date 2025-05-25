import requests

BASE_URL = "http://localhost:5000"

def debug_test():
    print("🔍 Debug API Test")
    
    # Test root
    response = requests.get(f"{BASE_URL}/")
    print(f"Root: {response.status_code} - {response.json()}")
    
    # Test restaurants with debugging
    response = requests.get(f"{BASE_URL}/api/restaurants")
    print(f"Restaurants Status: {response.status_code}")
    print(f"Restaurants Headers: {response.headers.get('content-type')}")
    print(f"Restaurants Response: {response.text[:200]}...")  # First 200 chars
    
    # Test users with debugging  
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Users Status: {response.status_code}")
    print(f"Users Response: {response.text[:200]}...")

if __name__ == "__main__":
    debug_test()
