import streamlit as st
import json
st.set_page_config(page_title="WatchGrid")

st.title("📽️WatchGrid")
st.subheader("Your personal movie space. Coming Soon!")

with open("data/movies.json") as f:
    movies = json.load(f)

# st.subheader("Popular picks")
cols = st.columns(5)
for idx, movie in enumerate(movies):
    with cols[idx%5]:
        st.image(movie["image_url"])
        st.write(movie["title"])
        st.write(movie["release_date"], movie["language"])
