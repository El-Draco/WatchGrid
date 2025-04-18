import streamlit as st
import asyncio
from models.movie import Movie
from core.settings import settings
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="WatchGrid")
st.title("📽️ WatchGrid")
st.subheader("Popular Picks")

async def fetch_movies():
    conn = await settings.get_connection()
    try:
        rows = await conn.fetch("SELECT * FROM Movie LIMIT 10")
        return [Movie(**dict(r)) for r in rows]
    finally:
        await conn.close()


# Call async inside Streamlit
movies = asyncio.run(fetch_movies())

cols = st.columns(5)
for idx, movie in enumerate(movies):
    with cols[idx % 5]:
        try:
            # try to load the img one by one w some small delay
            time.sleep(0.2)
            st.image(movie.image_url, width=150)
        except:
            st.image("https://via.placeholder.com/150?text=No+Image", width=150)

        # Text info
        st.markdown(f"**{movie.title}**")
        st.caption(f"📅 {movie.release_date} | 🌐 {movie.language} | ⭐ {movie.avg_rating}")
