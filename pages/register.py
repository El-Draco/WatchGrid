import streamlit as st
from core.auth import register_user
import time
with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")
    

st.title("Create a New WatchGrid Account ✨")


first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
dob = st.date_input("Date of Birth")

if st.button("Register"):
    register_user(email, password, first_name, last_name, dob.strftime("%Y-%m-%d"))
    time.sleep(0.5)
    # st.rerun()  # Rerun app to refresh session state
    st.switch_page("app.py")
