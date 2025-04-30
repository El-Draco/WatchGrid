import streamlit as st
from models.movie import Movie
from core.settings import settings
from loguru import logger
from core.auth import is_logged_in, get_current_user

# Setup
st.set_page_config(page_title="Movie Info", page_icon="🎥")

# Sidebar
with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎥 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")

# Get the movie ID from the URL query parameters
movie_id = st.query_params.get("movie_id")

if not movie_id:
    st.error("Movie ID not provided!")
else:
    # Function to fetch movie info from the database
    def fetch_movie_info(movie_id):
        conn = settings.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Movie WHERE movie_id = :movie_id", {"movie_id": movie_id})
            row = cursor.fetchone()

            if row:
                movie_data = {
                    "movie_id": row[0],
                    "title": row[1],
                    "release_date": row[2],
                    "duration": row[3],
                    "language": row[4],
                    "image_url": row[5],
                    "avg_rating": row[6]
                }
                return Movie(**movie_data)
            else:
                st.error(f"No movie found with ID {movie_id}")
                return None
        except Exception as e:
            st.error(f"Failed to fetch movie info: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

# Fetch Watchlists


# Fetch the movie details
movie = fetch_movie_info(movie_id)

if movie:
    # Display Movie Title
    st.title(movie.title)

    # Display movie image
    st.image(movie.image_url, use_container_width=True, width=150)

    # Button to add to a watchlist
    #st.selectbox("Add to watchlist", )

    # Movie details
    st.subheader("Movie Details")
    st.markdown(f"**Release Date:** {movie.release_date}")
    st.markdown(f"**Duration:** {movie.duration} minutes")
    st.markdown(f"**Language:** {movie.language}")
    st.markdown(f"**Average Rating:** {movie.avg_rating} ⭐")

else:
    st.error("Error: Movie data could not be fetched.")
