import streamlit as st
from core.auth import is_logged_in
from core.settings import settings
from models.movie import Movie

st.set_page_config(page_title="Add Movie", page_icon="➕")
st.title("➕ Add a Movie")

user_id = '44d7ac2e-ca82-4602-8816-029bf464ae46'  # your user id

def search_movies(title):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT MOVIE_ID, TITLE, RELEASE_DATE, DURATION, LANGUAGE, IMAGE_URL, AVG_RATING
            FROM MOVIE
            WHERE TITLE LIKE :title
        """, {"title": f"%{title}%"})
        movies = []
        for row in cursor.fetchall():
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
    except:
        return []
    finally:
        cursor.close()
        conn.close()
#
# if not is_logged_in():
#     st.warning("Please login to add movies.")
#     st.stop()

title = st.text_input("Enter Movie Title:")

if st.button("Search"):
    if title:
        results = search_movies(title)
        if results:
            st.session_state.search_results = results
            st.switch_page("pages/searchResults.py")
        else:
            st.warning("No results found.")
    else:
        st.warning("Please enter a title.")
