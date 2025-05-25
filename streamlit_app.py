import streamlit as st
from ui.components import show_restaurant_grid, show_booking_form, show_chat_interface

# Page config
st.set_page_config(
    page_title="FoodieSpot AI Reservations",
    page_icon="🍽️",
    layout="wide"
)

def main():
    st.title("🍽️ FoodieSpot - AI Restaurant Reservations")
    
    # Navigation
    tab1, tab2 = st.tabs(["🍽️ Browse & Book", "🤖 AI Chat"])
    
    with tab1:
        # Initialize session state
        if "selected_restaurant" not in st.session_state:
            st.session_state.selected_restaurant = None
        
        # Show booking form if restaurant selected
        if st.session_state.selected_restaurant:
            if st.button("← Back to Restaurants"):
                st.session_state.selected_restaurant = None
                st.rerun()
            
            booking_success = show_booking_form(st.session_state.selected_restaurant)
            if booking_success:
                st.session_state.selected_restaurant = None  # Reset after booking
        else:
            # Show restaurant grid
            selected = show_restaurant_grid()
            if selected:
                st.session_state.selected_restaurant = selected
                st.rerun()
    
    with tab2:
        show_chat_interface()

if __name__ == "__main__":
    main()
