import streamlit as st
from core.auth import is_logged_in
from models.movie import Movie
from core.settings import settings
from loguru import logger
# 1. Setup
st.set_page_config(page_title="WatchGrid", page_icon="🎬")

# 2. Header Section
# 2. Header Section
with st.container():
    col1, col2 = st.columns([6, 2.9])
    with col1:
        st.markdown("## 🎥 WatchGrid")
    with col2:
        st.write("")  # minor vertical spacing
        if is_logged_in():
            if st.button("Logout"):
                st.switch_page("pages/logout.py")
        else:
            login_col1, login_col2 = st.columns([1, 1], gap="small")
            with login_col1:
                if st.button("Login"):
                    st.switch_page("pages/login.py")
            with login_col2:
                if st.button("Register"):
                    st.switch_page("pages/register.py")





# 3. Sidebar
with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")

# if is_logged_in():
    # st.markdown(f"#### 👋 Hello, User {st.session_state['user_id']}")


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

cols = st.columns(5)

for idx, movie in enumerate(movies):
    with cols[idx % 5]:
        with st.container():
            try:
                if movie.image_url:
                    st.image(movie.image_url, width=150)
                else:
                    st.image("https://via.placeholder.com/150?text=No+Image", width=150)
            except:
                st.image("https://via.placeholder.com/150?text=No+Image", width=150)

            title = movie.title
            if len(title) > 20:
                title = title[:17] + "..."

            st.markdown(f"<h5 style='text-align: center;'>{title}</h5>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 12px;'>📅 {movie.release_date}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 12px;'>🌐 {movie.language} | ⭐ {movie.avg_rating}</div>", unsafe_allow_html=True)
