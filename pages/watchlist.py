import streamlit as st
from core.auth import is_logged_in

st.title("🎬 My Watchlists")

with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")

if st.button("➕ Add Movie to Watchlist"):
    st.switch_page("pages/search.py") #adding the + add movie button 

if not is_logged_in():
    st.warning("Please login to access your Watchlists.")
    st.stop()

st.success("Here are your personal Watchlists!")
# Show actual watchlist stuff here
