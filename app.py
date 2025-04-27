import time
import streamlit as st
from core.auth import is_logged_in
from models.movie import Movie
from core.settings import settings
from loguru import logger

# 1. Setup
st.set_page_config(
    page_title="WatchGrid",
    page_icon="🎥",
    layout="wide",  # Important for mobile
    initial_sidebar_state="expanded"
)

# Inject responsive CSS
st.markdown("""
    <style>
    img {
        max-width: 100%;
        height: auto;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    @media only screen and (max-width: 768px) {
        html, body, [class*="css"]  {
            font-size: 16px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 2. Header Section
with st.container():
    col1, col2 = st.columns([6, 3])
    with col1:
        st.write("")
        st.markdown("## 🎥 WatchGrid")
    with col2:
        st.write("")  # minor spacing

        # Center align the login/register buttons
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if is_logged_in():
            if st.button("Logout", use_container_width=True):
                st.switch_page("pages/logout.py")
        else:
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/login.py")
            if st.button("Register", use_container_width=True):
                st.switch_page("pages/register.py")
        st.markdown("</div>", unsafe_allow_html=True)



# 3. Sidebar
with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎥 Watchlists")

# 4. Main Content
st.subheader("Popular Picks")

def fetch_movies():
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Movie FETCH FIRST 10 ROWS ONLY")
        rows = cursor.fetchall()
        movies = []
        for row in rows:
            movie_data = {
                "movie_id": row[0],
                "title": row[1],
                "release_date": row[2],
                "duration": row[3],
                "language": row[4],
                "image_url": row[5],
                "avg_rating": row[6]
            }
            movies.append(Movie(**movie_data))
        return movies
    except Exception as e:
        st.error(f"Failed to load movies: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

movies = fetch_movies()

# Adjust number of columns depending on screen size
# (5 for large, 2 or 3 will feel better for mobile when layout=wide)
cols = st.columns(2 if len(movies) <= 4 else 5)

for idx, movie in enumerate(movies):
    with cols[idx % len(cols)]:
        with st.container():
            try:
                if movie.image_url:
                    st.image(movie.image_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)
                    time.sleep(0.1)
            except:
                st.image("https://via.placeholder.com/150?text=No+Image", use_column_width=True)

            title = movie.title
            if len(title) > 20:
                title = title[:17] + "..."

            st.markdown(f"<h5 style='text-align: center;'>{title}</h5>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 12px;'>🗕️ {movie.release_date}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 12px;'>🌐 {movie.language} | ⭐ {movie.avg_rating}</div>", unsafe_allow_html=True)
