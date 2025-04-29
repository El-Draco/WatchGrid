import streamlit as st

st.set_page_config(page_title="Movie Details", page_icon="🎥")
st.title("🎥 Movie Details")

if "selected_movie" not in st.session_state or st.session_state.selected_movie is None:
    st.warning("No movie selected.")
    st.stop()

movie = st.session_state.selected_movie

st.image(movie.image_url or "https://via.placeholder.com/150", use_container_width=True)
st.header(movie.title)

st.markdown(f"""
**Release Date:** {movie.release_date}  
**Duration:** {movie.duration} minutes  
**Language:** {movie.language}  
**Average Rating:** ⭐ {movie.avg_rating}
""")

if st.button("⬅️ Back to Watchlists"):
    st.session_state.selected_movie = None
    st.switch_page("pages/watchlist.py")
