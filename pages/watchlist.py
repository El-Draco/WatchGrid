import streamlit as st
from core.auth import is_logged_in
from core.settings import settings
from models.movie import Movie
import matplotlib.pyplot as plt


st.set_page_config(page_title="Watchlist", page_icon="🎬")
st.title("🎬 My Watchlists")

user_id = '44d7ac2e-ca82-4602-8816-029bf464ae46'  # your current user id

# Helpers
def get_watchlist_id(user_id, status):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT WATCHLIST_ID FROM WATCHLIST WHERE USER_ID = :user_id AND WATCH_STATUS = :status
        """, {"user_id": user_id, "status": status})
        return cursor.fetchone()[0]
    except:
        return None
    finally:
        cursor.close()
        conn.close()

def fetch_movies(watchlist_id):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT MOVIE.MOVIE_ID, TITLE, RELEASE_DATE, DURATION, LANGUAGE, IMAGE_URL, AVG_RATING
            FROM WATCHLIST_MOVIES JOIN MOVIE ON WATCHLIST_MOVIES.MOVIE_ID = MOVIE.MOVIE_ID
            WHERE WATCHLIST_MOVIES.WATCHLIST_ID = :watchlist_id
        """, {"watchlist_id": watchlist_id})
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

def movie_grid(movies):
    cols = st.columns(5)
    for idx, movie in enumerate(movies):
        with cols[idx % 5]:
            st.image(movie.image_url or "https://via.placeholder.com/150", use_container_width=True)
            st.markdown(f"**{movie.title[:25]}**")
            st.caption(f"🗓 {movie.release_date} | 🌐 {movie.language} | ⭐ {movie.avg_rating}")
            if st.button("📽️ View", key=f"watchlist_view_{movie.movie_id}"):
                st.session_state.selected_movie = movie
                st.switch_page("pages/viewMovie.py")

status_map = {
    'Plan to Watch': 'PLAN',
    'On Hold': 'HOLD',
    'Watching': 'WATCH',
    'Completed': 'COMPLETE',
    'Dropped': 'DROP'
}

def listDistribution():
    conn = settings.get_connection()
    cursor = conn.cursor()
    counts = []
    try:
        for status in status_map.values():  # Iterate through each status in the map
            cursor.execute("""
                SELECT COUNT(*) FROM WATCHLIST 
                WHERE USER_ID = :user_id AND WATCH_STATUS = :status 
                GROUP BY WATCH_STATUS
            """, {"user_id": user_id, "status": status})
            
            result = cursor.fetchall()  # Get the count for this status
            if result:  # Ensure the query returned a result
                counts.append(result[0][0])  # Append the count to the list

        return counts  # Return the list of counts

    except:
        return []
    finally:
        cursor.close()
        conn.close()

distribution = listDistribution()

def plotDistribution(distribution):
    if not distribution:
        st.write("No data to display.")
        return

    fig, ax = plt.subplots(figsize=(1, 1))

    wedges, texts, autotexts = ax.pie(
        distribution,
        labels=status_map.keys(),
        autopct='%1.0f%%',
        startangle=90,
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'],
        textprops={'fontsize': 4},
    )

    ax.set_title('Watch Status', fontsize=4)

    ax.axis('equal')

    st.pyplot(fig)

# Main
# if not is_logged_in():
#     st.warning("Please login to access Watchlists.")
#     st.stop()


with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎥 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")

plotDistribution(distribution)


selected_status = st.selectbox("Select Watchlist:", list(status_map.keys()))
watchlist_id = get_watchlist_id(user_id, status_map[selected_status])

if watchlist_id:
    movies = fetch_movies(watchlist_id)
    if movies:
        movie_grid(movies)
    else:
        st.info("No movies yet in this list.")
else:
    st.error("Failed to load watchlist.")

st.markdown("---")
if st.button("➕ Add a Movie to this Watchlist", use_container_width=True):
    st.switch_page("pages/addMovie.py")
