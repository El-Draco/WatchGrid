import streamlit as st
from core.auth import is_logged_in
from core.settings import settings
from models.movie import Movie
import time

# user_id = st.session_state["user_id"]
user_id = '44d7ac2e-ca82-4602-8816-029bf464ae46'

st.title("🎬 My Watchlists")

def search_movies(title):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT MOVIE_ID, TITLE, RELEASE_DATE, DURATION, LANGUAGE, IMAGE_URL, AVG_RATING
            FROM MOVIE
            WHERE LOWER(TITLE) LIKE :title
        """
        cursor.execute(query, {"title": "%" + title + "%"})
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
        st.error(f"Failed to load searched movies: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

cols = st.columns(5)

def show_movies(movies):
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
                    print("HERE1")
                    if st.button(f"📽️ {movie.title}", key = movie.movie_id):
                        print("HERE2")
                        st.session_state.selected_movie = movie
                        st.switch_page("viewMovie.py")



with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")

with st.container():
    st.header("Add Movie")
    title = st.text_input("Enter movie title")

    if st.button("Search"):
        if title:
            movies = search_movies(title)
            if movies:
                st.subheader(f"Search Results for '{title}':")
                show_movies(movies)
            else:
                st.warning("No movies found with that title.")
        else:
            st.warning("Please enter a movie title to search.")
        