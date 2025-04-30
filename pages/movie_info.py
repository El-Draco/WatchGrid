import streamlit as st
from models.movie import Movie
from models.review import Review 
from core.settings import settings
from datetime import date

# Setup
st.set_page_config(page_title="Movie Info", page_icon="🎥")

# Sidebar
with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎥 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")

# user ID (can be changed to fetch user_id from session)
user = '44d7ac2e-ca82-4602-8816-029bf464ae46'

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

def fetch_movie_genre(movie_id):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        # First, fetch the genre IDs associated with the movie
        cursor.execute("SELECT genre_id FROM ISGENRE WHERE movie_id = :movie_id", {"movie_id": movie_id})
        rows = cursor.fetchall()

        if rows:
            # Extract genre IDs from rows
            genre_ids = [str(row[0]) for row in rows]

            # Join genre_ids into a comma-separated string for the IN clause
            genre_ids_str = ",".join(genre_ids)

            # Use the 'IN' clause to fetch genre names for all genre_ids
            cursor.execute(f"SELECT genre_name FROM GENRE WHERE genre_id IN ({genre_ids_str})")
            genre_names = cursor.fetchall()

            # Return the list of genre names
            return [genre[0] for genre in genre_names]
        else:
            st.error(f"No genre found for movie")
            return None
    except Exception as e:
        st.error(f"Failed to fetch movie genre: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def fetch_movie_tags(movie_id):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        # First, fetch the TAG IDs associated with the movie
        cursor.execute("SELECT tag_id FROM HASTAGS WHERE movie_id = :movie_id", {"movie_id": movie_id})
        rows = cursor.fetchall()

        if rows:
            # Extract TAG IDs from rows
            tag_ids = [str(row[0]) for row in rows]

            # Join genre_ids into a comma-separated string for the IN clause
            tag_ids_str = ",".join(tag_ids)

            # Use the 'IN' clause to fetch genre names for all genre_ids
            cursor.execute(f"SELECT tag_text FROM TAG WHERE tag_id IN ({tag_ids_str})")
            tag_names = cursor.fetchall()

            # Return the list of genre names
            return [tag[0] for tag in tag_names]
        else:
            st.error(f"No tags found for movie")
            return None
    except Exception as e:
        st.error(f"Failed to fetch movie tags: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Fetch Watchlists
def get_watchlists(user_id):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT WATCHLIST_ID, TITLE 
            FROM WATCHLIST 
            WHERE USER_ID = :user_id
        """, {"user_id": user_id})
        
        rows = cursor.fetchall()
        return [{"watchlist_id": row[0], "title": row[1]} for row in rows]
    except Exception as e:
        print(f"Error fetching watchlists: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Get titles of watchlists
watchlists = get_watchlists(user)
watchlists_titles = [wl["title"] for wl in watchlists]

def add_movie_to_watchlist(selected_watchlist, selected_watchlist_id, movie_id):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO WATCHLIST_MOVIES (watchlist_id, movie_id)
            VALUES (:watchlist_id, :movie_id)
        """, {"watchlist_id": selected_watchlist_id, "movie_id": movie_id})
        conn.commit()
        st.success(f"Movie added to watchlist: {selected_watchlist} ")
    except Exception as e:
        st.error(f"Movie already in watchlist: {selected_watchlist}")
    finally:
        cursor.close()
        conn.close()


# Fetch the movie details
movie = fetch_movie_info(movie_id)

if movie:
    # Display Movie Title
    st.title(movie.title)

    # Display movie image
    st.image(movie.image_url, use_container_width=True, width=150)

    # Button to add to a watchlist
    if watchlists:
        selected_watchlist = st.selectbox("Add to watch list:", watchlists_titles, index = None, placeholder = "Add to watch list", label_visibility = "hidden")
        selected_watchlist_id = next ((wl["watchlist_id"] for wl in watchlists if wl["title"] == selected_watchlist), None)
        # Adding movies to selected watchlist
        if selected_watchlist:
            add_movie_to_watchlist(selected_watchlist, selected_watchlist_id, movie_id)
    else:
        st.warning("No watchlists found for this user.")

    # Movie details
    st.subheader("Movie Details")
    st.markdown(f"**Release Date:** {movie.release_date}")
    st.markdown(f"**Duration:** {movie.duration} minutes")
    st.markdown(f"**Language:** {movie.language}")
    st.markdown(f"**Average Rating:** {movie.avg_rating} ⭐")

    movie_genre = fetch_movie_genre(movie_id)
    if movie_genre:
        st.markdown(f"**Genre:** {', '.join(movie_genre)}")

    movie_tags = fetch_movie_tags(movie_id)
    if movie_tags:
        st.markdown(f"**Tags:** {', '.join(movie_tags)}")

else:
    st.error("Error: Movie data could not be fetched.")

st.subheader("Reviews")
# Review submitting
def add_review_to_movie(review_data: Review):
    conn = settings.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Review (review_id, user_id, movie_id, platform_id, rating, review_date, headline, review_text, review_body)
            VALUES (Review_SEQ.NEXTVAL, :user_id, :movie_id, :platform_id, :rating, SYSDATE, :headline, :review_text, :review_body)
        """, {
            "user_id": review_data.user_id,
            "movie_id": review_data.movie_id,
            "platform_id": review_data.platform_id,
            "rating": review_data.rating,
            "headline": review_data.headline,
            "review_text": review_data.review_text,
            "review_body": review_data.review_body
        })
        conn.commit()
        st.success("Review added successfully!")
    
    except Exception as e:
        conn.rollback()
        st.error(f"Failed to add review: {e}")
    
    finally:
        cursor.close()
        conn.close()

# form
def insert_review_to_db(review: Review):
    conn = settings.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO REVIEW (review_id, user_id, movie_id, platform_id, rating, review_date, headline, review_text, review_body)
            VALUES (REVIEW_SEQ.NEXTVAL, :user_id, :movie_id, :platform_id, :rating, :review_date, :headline, :review_text, :review_body)
        """, {
            "user_id": review.user_id,
            "movie_id": review.movie_id,
            "platform_id": review.platform_id,
            "rating": review.rating,
            "review_date": review.review_date,
            "headline": review.headline,
            "review_text": review.review_text,
            "review_body": review.review_body
        })
        conn.commit()
        st.success("Review submitted successfully!")
    except Exception as e:
        st.error(f"Failed to submit review: {e}")
    finally:
        cursor.close()
        conn.close()

if "show_review_form" not in st.session_state:
    st.session_state.show_review_form = False

if st.button("Add a Review"):
    st.session_state.show_review_form = True

if st.session_state.show_review_form:
    st.subheader("Write Your Review")

    user_id = user
    platform_id = st.selectbox("Platform ID", [1, 2, 3])
    rating = st.slider("Rating", 0.0, 10.0, 5.0, step=0.1)
    headline = st.text_input("Headline")
    review_text = st.text_area("Short Summary")
    review_body = st.text_area("Full Review")

    if st.button("Submit Review"):
        if user_id:
            review_data = Review(
                review_id=0,
                user_id=user_id,
                movie_id=movie_id,
                platform_id=platform_id,
                rating=rating,
                review_date=date.today(),
                headline=headline,
                review_text=review_text,
                review_body=review_body
            )
            insert_review_to_db(review_data)
            st.session_state.show_review_form = False
        else:
            st.error("You must be logged in to leave a review.")

# Review section
def fetch_reviews_by_movie(movie_id: int):
    conn = settings.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT r.review_id, r.user_id, r.rating, r.review_date, r.headline, r.review_text, r.review_body
            FROM Review r
            WHERE r.movie_id = :movie_id
            ORDER BY r.review_date DESC
        """, {"movie_id": movie_id})
        
        rows = cursor.fetchall()
        
        if rows:
            reviews = []
            for row in rows:
                review = {
                    "review_id": row[0],
                    "user_id": row[1],
                    "rating": row[2],
                    "review_date": row[3],
                    "headline": row[4],
                    "review_text": row[5],
                    "review_body": row[6]
                }
                reviews.append(review)
            return reviews
        else:
            return None  # No reviews found
    
    except Exception as e:
        st.error(f"Failed to fetch reviews: {e}")
        return None
    
    finally:
        cursor.close()
        conn.close()

reviews = fetch_reviews_by_movie(movie_id)

if reviews:
    for review in reviews:
        st.markdown(f"**Review by** {review['user_id']}")
        st.markdown(f"**Rating:** {review['rating']}/10")
        st.markdown(f"**Date:** {review['review_date']}")
        if review['headline']:
            st.markdown(f"**Headline:** {review['headline']}")
        if review['review_text']:
            st.markdown(f"**Review Text:** {review['review_text']}")
        if review['review_body']:
            st.markdown(f"**Review Body:** {review['review_body']}")
        st.markdown("-------------------------------------------")
else:
    st.write("No reviews found for this movie.")
