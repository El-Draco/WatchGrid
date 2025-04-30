import streamlit as st
from core.db import get_movie_by_title

st.set_page_config(page_title="Search", page_icon="🔎")
st.title("🔎 Search for a Movie")

with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")

movie_name = st.text_input("Enter movie name:")
search_clicked = st.button("Search")

if search_clicked:
    result = get_movie_by_title(movie_name)

    if result:
        movie_id, title = result
        st.success(f"✅ Movie found: {title}")
        # Simulate redirect (replace with actual page later)
        st.markdown(f"[👉 Go to Movie Page](pages/movie_details.py?movie_id={movie_id})")
    else:
        st.error("❌ Invalid movie name. Please try again.")

