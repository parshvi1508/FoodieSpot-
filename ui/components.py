import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict
from .services import get_restaurants, check_availability, make_reservation

def show_restaurant_grid():
    """Display restaurant cards and handle selection"""
    restaurants = get_restaurants()
    
    if not restaurants:
        st.warning("No restaurants available")
        return None
    
    st.subheader(f"🍽️ Available Restaurants ({len(restaurants)})")
    
    # Create grid layout
    cols = st.columns(2)
    
    for idx, restaurant in enumerate(restaurants):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"""
                **{restaurant['name']}** 🍽️  
                📍 {restaurant['location']} | 🍜 {restaurant['cuisine']}  
                👥 Capacity: {restaurant['capacity']} | ✅ Tables: {restaurant['available_tables']}
                """)
                
                if st.button(f"Book {restaurant['name']}", key=f"book_{restaurant['id']}", use_container_width=True):
                    return restaurant
    return None

def show_booking_form(restaurant: Dict):
    """Show booking form for selected restaurant"""
    st.success(f"Booking: **{restaurant['name']}** 🎯")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input("Name*", placeholder="John Doe")
            user_phone = st.text_input("Phone*", placeholder="1234567890")
            party_size = st.selectbox("Party Size*", range(1, 11), index=3)
        
        with col2:
            user_email = st.text_input("Email", placeholder="john@example.com")
            min_date = datetime.now().date() + timedelta(days=1)
            booking_date = st.date_input("Date*", min_value=min_date)
            time_slots = ["17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00"]
            booking_time = st.selectbox("Time*", time_slots, index=4)
        
        if st.form_submit_button("🔍 Check Availability & Book", use_container_width=True):
            if not user_name or not user_phone:
                st.error("Please fill required fields (Name & Phone)")
                return False
            
            # Check availability
            with st.spinner("Checking availability..."):
                availability = check_availability(
                    restaurant['id'], party_size, 
                    booking_date.strftime("%Y-%m-%d"), booking_time
                )
            
            if availability.get('available'):
                # Make reservation
                reservation = make_reservation(
                    user_name, user_phone, restaurant['id'],
                    availability['suggested_table_id'], party_size,
                    booking_date.strftime("%Y-%m-%d"), booking_time, user_email
                )
                
                if reservation.get('success'):
                    st.balloons()
                    st.success(f"""
                    🎉 **Reservation Confirmed!**
                    
                    **ID:** {reservation['reservation_id']}  
                    **Restaurant:** {restaurant['name']}  
                    **Date:** {booking_date} at {booking_time}  
                    **Party:** {party_size} people  
                    **Name:** {user_name}
                    """)
                    return True
                else:
                    st.error(f"Booking failed: {reservation.get('error', 'Unknown error')}")
            else:
                st.warning("❌ No tables available. Try different time.")
            
            return False

def show_chat_interface():
    """Simple chat interface for AI integration"""
    st.subheader("🤖 AI Chat Assistant")
    st.info("💬 Example: 'Book table for 4 tomorrow at 7pm' or 'Show Italian restaurants'")
    
    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your booking assistant. How can I help?"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simulate AI response (will be real AI in Issue #4)
        with st.chat_message("assistant"):
            response = f"I understand: '{prompt}'. AI integration coming in Issue #4! 🚀"
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
