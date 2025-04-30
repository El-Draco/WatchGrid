import streamlit as st
from core.auth import login_user, is_logged_in
import time

st.title("Login to WatchGrid 🎬")

with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if login_user(email, password):
        # st.success("Logged in successfully!")
        time.sleep(0.5)
        # st.rerun()  # Rerun app to refresh session state
        st.switch_page("app.py")