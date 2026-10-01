import streamlit as st

from recommender import MovieRecommender

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")


@st.cache_resource
def load_recommender():
    return MovieRecommender()


rec = load_recommender()

st.title("🎬 Movie Recommendation System")
st.caption("Content-based filtering: TF-IDF on genres and plot + cosine similarity.")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    n = st.slider("Number of recommendations", 3, 10, 5)
    genre = st.selectbox("Filter by genre (optional)", ["Any"] + rec.genres)
    genre = None if genre == "Any" else genre
    st.caption(f"{len(rec.titles)} movies in the dataset")


def show(results):
    if results.empty:
        st.warning("No movies found. Try removing the genre filter.")
        return
    for _, r in results.iterrows():
        with st.container(border=True):
            st.markdown(f"**{r['title']}** ({r['year']})")
            st.caption(r["genres"].replace("|", " · "))
            st.write(r["description"])
            st.progress(min(float(r["score"]), 1.0), text=f"Match: {r['score'] * 100:.0f}%")


tab1, tab2 = st.tabs(["Based on movies I like", "Describe what I want"])

with tab1:
    liked = st.multiselect("Pick one or more movies you liked", rec.titles)
    if liked:
        show(rec.recommend(liked, n=n, genre=genre))
    else:
        st.info("Select at least one movie to get recommendations.")

with tab2:
    query = st.text_input("Describe a movie", placeholder="e.g. friends on a road trip, or a heist in space")
    if query.strip():
        show(rec.recommend_from_text(query, n=n, genre=genre))
    else:
        st.info("Type a few words about the kind of movie you want.")