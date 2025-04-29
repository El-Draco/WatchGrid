import streamlit as st
from core.auth import is_logged_in
from core.settings import settings
from models.movie import Movie
import time

# user_id = st.session_state["user_id"]
user_id = '44d7ac2e-ca82-4602-8816-029bf464ae46'

st.title("🎬 My Watchlists")

def get_watchlist_id(user_id, status):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT * FROM WATCHLIST 
            WHERE USER_ID = :user_id AND WATCH_STATUS = :status
        """
        cursor.execute(query, {"user_id": user_id, "status": status})
        row = cursor.fetchall()[0]
        watchlist_id = row[0]
        return watchlist_id
    except Exception as e:
        st.error(f"Failed to get watchlist id: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def fetch_movies(watchlist_id):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT MOVIE.MOVIE_ID, TITLE, RELEASE_DATE, DURATION, LANGUAGE, IMAGE_URL, AVG_RATING 
            FROM WATCHLIST_MOVIES 
            JOIN MOVIE ON WATCHLIST_MOVIES.MOVIE_ID = MOVIE.MOVIE_ID 
            WHERE WATCHLIST_MOVIES.WATCHLIST_ID = :watchlist_id
        """
        cursor.execute(query, {"watchlist_id": watchlist_id})
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
        st.error(f"Failed to load watchlist movies: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


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


watchlistOptions2status = {
    'Plan to Watch': 'PLAN',
    'On Hold': 'HOLD',
    'Watching': 'WATCH',
    'Completed': 'COMPLETE',
    'Dropped': 'DROP'
}

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
                    if st.button(f"📽️ {movie.title}"):
                        st.session_state.selected_movie = movie
                        st.session_state.page = "movie_details"
                    


# Components start here -----------------------------------------------------------------------

with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")

st.success("Here are your personal Watchlists!")

if is_logged_in():
    st.warning("Please login to access your Watchlists.")
    st.stop()
else:
    with st.container():
        st.markdown("""
        <style>
        div[data-baseweb="select"] {
            width: 175px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        watchlistOptions = st.selectbox(
            'Select a Watch List:',
            ['Plan to Watch', 'On Hold', 'Watching', 'Completed', 'Dropped']
        )

        show_movies(fetch_movies(get_watchlist_id(user_id, watchlistOptions2status[watchlistOptions])))

        if st.button("➕ Add Movie"):
            st.switch_page("./pages/addMovie.py")

