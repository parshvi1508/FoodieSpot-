import streamlit as st
from ui.components import show_main_interface

# Professional page configuration
st.set_page_config(
    page_title="FoodieSpot - Premium Restaurant Reservations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    print("[DEBUG] Starting professional restaurant booking app")
    
    # Hide Streamlit default elements for cleaner look
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > div:first-child {margin-top: -80px;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Show professional main interface
    show_main_interface()

if __name__ == "__main__":
    main()
