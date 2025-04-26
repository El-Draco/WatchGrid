import streamlit as st
from core.auth import is_logged_in, logout_user
import time

st.set_page_config(page_title="WatchGrid", page_icon="🎥")

# Sidebar (optional if you want users to still navigate)
with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")

# Immediately logout
if is_logged_in():
    logout_user()
    st.success("Logged out successfully!")
    time.sleep(1)  # Give 1 second to show success message
    st.switch_page("app.py")
else:
    st.warning("You are already logged out.")
    time.sleep(1)
    st.switch_page("app.py")
