import requests
import streamlit as st
from typing import Dict, List

BASE_URL = "http://localhost:5000"

@st.cache_data(ttl=60)
def get_restaurants() -> List[Dict]:
    """Get all restaurants with caching"""
    try:
        response = requests.get(f"{BASE_URL}/api/restaurants")
        if response.status_code == 200:
            return response.json().get('restaurants', [])
        return []
    except Exception as e:
        st.error(f"Error fetching restaurants: {e}")
        return []

def check_availability(restaurant_id: int, party_size: int, date: str, time: str) -> Dict:
    """Check table availability"""
    try:
        payload = {"restaurant_id": restaurant_id, "party_size": party_size, "date": date, "time": time}
        response = requests.post(f"{BASE_URL}/api/check_availability", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def make_reservation(user_name: str, user_phone: str, restaurant_id: int, 
                    table_id: int, party_size: int, date: str, time: str, user_email: str = "") -> Dict:
    """Create a new reservation"""
    try:
        payload = {
            "user_name": user_name, "user_phone": user_phone, "user_email": user_email,
            "restaurant_id": restaurant_id, "table_id": table_id, 
            "party_size": party_size, "date": date, "time": time
        }
        response = requests.post(f"{BASE_URL}/api/make_reservation", json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
