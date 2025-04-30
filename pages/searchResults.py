import streamlit as st

st.set_page_config(page_title="Search Results", page_icon="🔎")
st.title("🔎 Search Results")

if "search_results" not in st.session_state or not st.session_state.search_results:
    st.warning("No search results available.")
    st.stop()

results = st.session_state.search_results

cols = st.columns(5)
for idx, movie in enumerate(results):
    with cols[idx % 5]:
        st.image(movie.image_url or "https://via.placeholder.com/150", use_container_width=True)
        # st.markdown(f"**{movie.title[:25]}**")
        st.caption(f"🗓 {movie.release_date} | 🌐 {movie.language} | ⭐ {movie.avg_rating}")
        movie_info_url = f"/movie_info?movie_id={movie.movie_id}"
        st.markdown(
            f"<h6 style='text-align: center;'><a target='_self' style='text-decoration: none; color: white' href='{movie_info_url}'>{movie.title}</a></h5>",
            unsafe_allow_html=True)

        # if st.button("📽️ View", key=f"search_view_{movie.movie_id}"):
        #     st.session_state.selected_movie = movie
            # st.switch_page("pages/viewMovie.py")
