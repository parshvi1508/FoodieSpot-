import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict
from .services import get_restaurants, check_availability, make_reservation

def apply_custom_css():
    """Apply custom CSS for restaurant website styling"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Open+Sans:wght@300;400;600&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0;
    }
    
    /* Header Styles */
    .restaurant-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem 0;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .restaurant-subtitle {
        font-family: 'Open Sans', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Restaurant Card Styles */
    .restaurant-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #f0f2f6;
    }
    
    .restaurant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .restaurant-card-header {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1.5rem;
        position: relative;
    }
    
    .restaurant-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .restaurant-card-body {
        padding: 1.5rem;
    }
    
    .restaurant-info {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .info-item {
        display: flex;
        align-items: center;
        font-family: 'Open Sans', sans-serif;
        color: #5a6c7d;
    }
    
    .info-icon {
        margin-right: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* Button Styles */
    .book-button {
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-family: 'Open Sans', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        text-align: center;
        width: 100%;
    }
    
    .book-button:hover {
        background: linear-gradient(45deg, #229954, #27ae60);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(39, 174, 96, 0.3);
    }
    
    /* Chat Interface Styles */
    .chat-container {
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f8f9fa;
    }
    
    .chat-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        font-family: 'Open Sans', sans-serif;
        color: #7f8c8d;
        font-size: 1.1rem;
    }
    
    /* Form Styles */
    .booking-form {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }
    
    .form-section {
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }
    
    /* Success Message Styles */
    .success-message {
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 5px 20px rgba(39, 174, 96, 0.2);
    }
    
    .success-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Navigation Styles */
    .nav-container {
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .restaurant-title {
            font-size: 2.5rem;
        }
        
        .restaurant-info {
            grid-template-columns: 1fr;
        }
        
        .restaurant-card {
            margin: 1rem 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_restaurant_header():
    """Display restaurant website header"""
    st.markdown("""
    <div class="restaurant-header">
        <h1 class="restaurant-title">🍽️ FoodieSpot</h1>
        <p class="restaurant-subtitle">Discover & Book Amazing Dining Experiences</p>
    </div>
    """, unsafe_allow_html=True)

def show_restaurant_grid():
    """Display restaurant cards with professional styling"""
    print("[DEBUG] Loading restaurant grid with professional styling")
    restaurants = get_restaurants()
    print(f"[DEBUG] Found {len(restaurants)} restaurants")

    if not restaurants:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;">
            <h3 style="color: #7f8c8d; font-family: 'Open Sans', sans-serif;">🔍 No restaurants available</h3>
            <p style="color: #95a5a6;">Please try again later or contact support.</p>
        </div>
        """, unsafe_allow_html=True)
        return None

    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="font-family: 'Playfair Display', serif; color: #2c3e50; font-size: 2.5rem;">
            Featured Restaurants
        </h2>
        <p style="font-family: 'Open Sans', sans-serif; color: #7f8c8d; font-size: 1.1rem;">
            Choose from {len(restaurants)} exceptional dining destinations
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create responsive grid
    cols = st.columns(2)

    for idx, restaurant in enumerate(restaurants):
        with cols[idx % 2]:
            # Create restaurant card with professional styling
            card_html = f"""
            <div class="restaurant-card">
                <div class="restaurant-card-header">
                    <h3 class="restaurant-name">{restaurant['name']}</h3>
                </div>
                <div class="restaurant-card-body">
                    <div class="restaurant-info">
                        <div class="info-item">
                            <span class="info-icon">📍</span>
                            <span>{restaurant['location']}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">🍜</span>
                            <span>{restaurant['cuisine']}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">👥</span>
                            <span>{restaurant['capacity']} seats</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">✅</span>
                            <span>{restaurant['available_tables']} tables</span>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # Book button with proper styling
            if st.button(
                f"📅 Reserve Table", 
                key=f"book_{restaurant['id']}", 
                help=f"Book a table at {restaurant['name']}",
                use_container_width=True
            ):
                print(f"[DEBUG] Restaurant selected: {restaurant['name']} (ID: {restaurant['id']})")
                return restaurant

    return None

def show_booking_form(restaurant: Dict):
    """Show professional booking form"""
    print(f"[DEBUG] Showing professional booking form for: {restaurant['name']}")
    
    # Success header
    st.markdown(f"""
    <div style="background: linear-gradient(45deg, #3498db, #2980b9); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
        <h2 style="font-family: 'Playfair Display', serif; margin: 0;">🎯 Reserve Your Table</h2>
        <p style="font-family: 'Open Sans', sans-serif; margin: 0.5rem 0 0 0; opacity: 0.9;">
            {restaurant['name']} • {restaurant['location']} • {restaurant['cuisine']} Cuisine
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("professional_booking_form", clear_on_submit=False):
        # Personal Information Section
        st.markdown("""
        <div class="section-title">
            👤 Guest Information
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_name = st.text_input(
                "Full Name *", 
                placeholder="Enter your full name",
                help="Required for reservation confirmation"
            )
            user_phone = st.text_input(
                "Phone Number *", 
                placeholder="e.g., +1 (555) 123-4567",
                help="We'll contact you for confirmation"
            )

        with col2:
            user_email = st.text_input(
                "Email Address", 
                placeholder="your.email@example.com",
                help="Optional: For booking confirmations"
            )
            party_size = st.selectbox(
                "Party Size *", 
                range(1, 13), 
                index=3,
                help="Number of guests including yourself"
            )
        
        # Reservation Details Section
        st.markdown("""
        <div class="section-title">
            📅 Reservation Details
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            min_date = datetime.now().date() + timedelta(days=1)
            max_date = datetime.now().date() + timedelta(days=60)
            booking_date = st.date_input(
                "Preferred Date *", 
                min_value=min_date,
                max_value=max_date,
                help="Select your dining date"
            )

        with col4:
            time_slots = [
                "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", 
                "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM", "9:30 PM"
            ]
            booking_time = st.selectbox(
                "Preferred Time *", 
                time_slots, 
                index=4,
                help="Select your dining time"
            )

        # Special Requests
        special_requests = st.text_area(
            "Special Requests (Optional)",
            placeholder="Any special requirements? (e.g., window seat, high chair, allergies)",
            height=100,
            help="Let us know how we can make your experience special"
        )

        # Submit button with professional styling
        submitted = st.form_submit_button(
            "🍽️ Check Availability & Reserve", 
            use_container_width=True,
            type="primary"
        )

        if submitted:
            print(f"[DEBUG] Professional form submitted with data: Name={user_name}, Phone={user_phone}, Party={party_size}, Date={booking_date}, Time={booking_time}")
            
            # Validation
            if not user_name or not user_phone:
                st.error("❌ Please provide your name and phone number for the reservation.")
                return False

            if len(user_name.strip()) < 2:
                st.error("❌ Please enter a valid full name.")
                return False
                
            if len(user_phone.strip()) < 10:
                st.error("❌ Please enter a valid phone number.")
                return False

            # Convert time format
            time_24h = convert_time_to_24h(booking_time)

            # Check availability
            with st.spinner("🔍 Checking table availability..."):
                availability = check_availability(
                    restaurant['id'], 
                    party_size,
                    booking_date.strftime("%Y-%m-%d"), 
                    time_24h
                )

            print(f"[DEBUG] Availability check result: {availability}")

            if availability.get('available'):
                # Show professional confirmation
                st.markdown("""
                <div style="background: linear-gradient(45deg, #27ae60, #2ecc71); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
                    <h2 style="font-family: 'Playfair Display', serif; margin: 0 0 1rem 0;">✅ Table Available!</h2>
                    <p style="font-family: 'Open Sans', sans-serif; margin: 0; font-size: 1.1rem;">Perfect! We have a table ready for your party.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Professional booking summary
                with st.expander("📋 **Reservation Summary**", expanded=True):
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3498db;">
                        <h4 style="font-family: 'Playfair Display', serif; color: #2c3e50; margin-bottom: 1rem;">Your Reservation Details</h4>
                        <div style="font-family: 'Open Sans', sans-serif; line-height: 1.8;">
                            <strong>🍽️ Restaurant:</strong> {restaurant['name']}<br>
                            <strong>📍 Location:</strong> {restaurant['location']}<br>
                            <strong>👤 Guest Name:</strong> {user_name}<br>
                            <strong>📞 Contact:</strong> {user_phone}<br>
                            <strong>👥 Party Size:</strong> {party_size} {'person' if party_size == 1 else 'people'}<br>
                            <strong>📅 Date:</strong> {booking_date.strftime('%A, %B %d, %Y')}<br>
                            <strong>🕐 Time:</strong> {booking_time}<br>
                            {f"<strong>📝 Special Requests:</strong> {special_requests}<br>" if special_requests else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Final confirmation button
                if st.button("🎉 Confirm Reservation", type="primary", use_container_width=True):
                    print(f"[DEBUG] Final confirmation clicked")
                    with st.spinner("📝 Finalizing your reservation..."):
                        reservation = make_reservation(
                            user_name.strip(), 
                            user_phone.strip(), 
                            restaurant['id'],
                            availability['suggested_table_id'], 
                            party_size,
                            booking_date.strftime("%Y-%m-%d"), 
                            time_24h, 
                            user_email.strip() if user_email else ""
                        )

                    print(f"[DEBUG] Final reservation result: {reservation}")

                    if reservation.get('success'):
                        st.balloons()
                        st.markdown(f"""
                        <div class="success-message">
                            <h2 class="success-title">🎉 Reservation Confirmed!</h2>
                            <div style="font-family: 'Open Sans', sans-serif; font-size: 1.1rem; line-height: 1.6;">
                                <p><strong>Confirmation ID:</strong> #{reservation['reservation_id']}</p>
                                <p><strong>Restaurant:</strong> {restaurant['name']}</p>
                                <p><strong>Date & Time:</strong> {booking_date.strftime('%A, %B %d, %Y')} at {booking_time}</p>
                                <p><strong>Party Size:</strong> {party_size} {'guest' if party_size == 1 else 'guests'}</p>
                                <p style="margin-top: 1.5rem; font-size: 0.95rem;">
                                    📱 <strong>Important:</strong> Please arrive 10-15 minutes early<br>
                                    🆔 Bring a valid ID for verification<br>
                                    📞 Call us if you need to modify your reservation
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        return True
                    else:
                        st.error(f"❌ **Reservation Failed:** {reservation.get('error', 'Please try again or contact us directly.')}")
                        
            else:
                # Professional "no availability" message
                st.markdown("""
                <div style="background: linear-gradient(45deg, #e74c3c, #c0392b); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
                    <h3 style="font-family: 'Playfair Display', serif; margin: 0 0 1rem 0;">😞 No Tables Available</h3>
                    <p style="font-family: 'Open Sans', sans-serif; margin: 0;">Sorry, we don't have availability for your selected date and time.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Alternative suggestions with professional styling
                st.markdown("""
                <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin: 2rem 0; border-left: 4px solid #f39c12;">
                    <h4 style="font-family: 'Playfair Display', serif; color: #2c3e50; margin-bottom: 1.5rem;">💡 Alternative Options</h4>
                    <div style="font-family: 'Open Sans', sans-serif; color: #5a6c7d;">
                        <p>• Try a different time slot (we often have availability 30 minutes earlier or later)</p>
                        <p>• Consider booking for tomorrow or another date</p>
                        <p>• Check our other fantastic restaurants</p>
                        <p>• Call us directly - we might have last-minute availability</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            return False

def show_ai_chat():
    """Professional AI chat interface"""
    print("[DEBUG] Loading professional AI chat interface")
    
    # Professional chat header
    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <h2 class="chat-title">🤖 AI Concierge</h2>
            <p class="chat-subtitle">Get instant help with restaurant recommendations and bookings</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Controls with professional styling
    col1, col2 = st.columns([4, 1])
    with col1:
        st.info("💬 Ask me about restaurants, cuisines, availability, or help with booking!")
    with col2:
        if st.button("🔄 New Chat", help="Start a fresh conversation"):
            print("[DEBUG] Resetting professional chat")
            if "messages" in st.session_state:
                del st.session_state.messages
            if "ai_agent" in st.session_state:
                st.session_state.ai_agent.reset_conversation()
            st.rerun()

    # Initialize AI agent with professional error handling
    if "ai_agent" not in st.session_state:
        try:
            print("[DEBUG] Initializing AI agent for professional interface")
            with st.spinner("🤖 Connecting to AI concierge..."):
                from ai.agent import RestaurantAgent
                st.session_state.ai_agent = RestaurantAgent()
            print("[DEBUG] Professional AI agent initialized successfully")
            st.success("🚀 **AI Concierge Ready!** Ask me anything about restaurants and bookings.")
        except Exception as e:
            print(f"[DEBUG] Professional AI agent initialization failed: {e}")
            st.error(f"❌ **AI Concierge Temporarily Unavailable**")
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #856404; margin-bottom: 1rem;">🔧 Service Notice</h4>
                <p style="color: #856404; margin: 0;">Our AI concierge is currently being updated. Please use the "Browse & Book" tab for reservations, or contact us directly.</p>
            </div>
            """, unsafe_allow_html=True)
            return

    # Initialize chat history with professional welcome
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🍽️ **Welcome to FoodieSpot!** I'm your personal dining concierge. I can help you discover amazing restaurants, check availability, and make reservations. What type of dining experience are you looking for today?"
            }
        ]

    # Display chat messages with professional styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Professional chat input
    if prompt := st.chat_input("Ask about restaurants, cuisines, or make a booking..."):
        print(f"[DEBUG] Professional chat input: {prompt}")
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response with professional handling
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    response = st.session_state.ai_agent.chat(prompt)
                    st.markdown(response)
                    print(f"[DEBUG] Professional AI response: {response}")
                except Exception as e:
                    print(f"[DEBUG] Professional AI response error: {e}")
                    error_response = f"🔧 I'm experiencing a brief technical issue. Please try rephrasing your question or use our booking form directly."
                    st.markdown(error_response)
                    response = error_response

        # Add AI response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

def show_main_interface():
    """Professional main interface with restaurant-grade styling"""
    print("[DEBUG] Loading professional main interface")
    
    # Apply custom CSS
    apply_custom_css()
    
    # Show restaurant header
    show_restaurant_header()
    
    # Professional tab interface
    tab1, tab2 = st.tabs(["🍽️ Discover & Reserve", "🤖 AI Concierge"])
    
    with tab1:
        print("[DEBUG] Professional Browse & Book tab selected")
        
        # Initialize session state
        if "selected_restaurant" not in st.session_state:
            st.session_state.selected_restaurant = None
        
        if st.session_state.selected_restaurant:
            # Professional back button
            if st.button("← Back to Restaurant Gallery", help="Return to restaurant selection"):
                print("[DEBUG] Returning to professional restaurant gallery")
                st.session_state.selected_restaurant = None
                st.rerun()
            
            # Show professional booking form
            booking_success = show_booking_form(st.session_state.selected_restaurant)
            if booking_success:
                st.session_state.selected_restaurant = None
        else:
            # Show professional restaurant grid
            selected = show_restaurant_grid()
            if selected:
                st.session_state.selected_restaurant = selected
                st.rerun()
    
    with tab2:
        print("[DEBUG] Professional AI Concierge tab selected")
        show_ai_chat()

def convert_time_to_24h(time_12h):
    """Convert 12-hour time format to 24-hour"""
    try:
        time_obj = datetime.strptime(time_12h, "%I:%M %p")
        return time_obj.strftime("%H:%M")
    except:
        # Fallback for different formats
        if "pm" in time_12h.lower() or "PM" in time_12h:
            hour = int(time_12h.split(":")[0])
            if hour != 12:
                hour += 12
            return f"{hour}:00"
        else:
            hour = int(time_12h.split(":")[0])
            if hour == 12:
                hour = 0
            return f"{hour:02d}:00"
