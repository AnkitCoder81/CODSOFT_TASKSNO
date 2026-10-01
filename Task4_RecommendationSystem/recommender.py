"""
Task 4: Recommendation System (content-based filtering)

Idea: describe every movie as text (its genres + a short plot description),
turn that text into TF-IDF vectors, and measure how similar two movies are
with cosine similarity. Movies closest to the ones you liked are recommended.

Run in terminal:   python recommender.py
Run the web UI:    streamlit run app.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path(__file__).with_name("movies.csv")


def _movie_text(row):
    """Genres are repeated 3 times so they count more than plot words."""
    genres = [g.replace("-", "").lower() for g in row["genres"].split("|")]
    return " ".join(genres * 3) + " " + row["description"]


class MovieRecommender:
    def __init__(self, csv_path=DATA_FILE):
        self.movies = pd.read_csv(csv_path)
        self.movies["text"] = self.movies.apply(_movie_text, axis=1)

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.movies["text"])
        self.similarity = cosine_similarity(self.matrix)  # movie x movie

        self.titles = self.movies["title"].tolist()
        self.genres = sorted({g for gs in self.movies["genres"] for g in gs.split("|")})

    # ------------------------------------------------------------------
    def _top(self, scores, n, exclude=(), genre=None):
        """Turn a score per movie into the top-n result table."""
        result = self.movies.copy()
        result["score"] = scores
        result = result[~result["title"].isin(exclude)]
        if genre:
            result = result[result["genres"].str.split("|").apply(lambda g: genre in g)]
        result = result.sort_values("score", ascending=False).head(n)
        return result[["title", "year", "genres", "description", "score"]].reset_index(drop=True)

    def recommend(self, liked_titles, n=5, genre=None):
        """Recommend movies similar to one or more liked movies."""
        idx = [self.titles.index(t) for t in liked_titles]
        scores = np.asarray(self.similarity[idx].mean(axis=0)).ravel()
        return self._top(scores, n, exclude=liked_titles, genre=genre)

    def recommend_from_text(self, query, n=5, genre=None):
        """Recommend movies that match a free-text description."""
        query_vec = self.vectorizer.transform([query.lower()])
        scores = cosine_similarity(query_vec, self.matrix).ravel()
        return self._top(scores, n, genre=genre)


# ----------------------------------------------------------------------
# Terminal version
# ----------------------------------------------------------------------
def main():
    rec = MovieRecommender()
    print(f"Loaded {len(rec.titles)} movies.")
    print("Type a movie you liked (exact title), or 'list' to see titles, 'quit' to exit.\n")
    lower = {t.lower(): t for t in rec.titles}

    while True:
        text = input("Movie you liked: ").strip()
        if text.lower() in {"quit", "exit"}:
            break
        if text.lower() == "list":
            print(", ".join(rec.titles), "\n")
            continue
        if text.lower() not in lower:
            print("Title not found. Type 'list' to see all titles.\n")
            continue

        result = rec.recommend([lower[text.lower()]], n=5)
        print(f"\nBecause you liked {lower[text.lower()]}, you may enjoy:")
        for i, r in result.iterrows():
            print(f"  {i + 1}. {r['title']} ({r['year']}) - {r['genres'].replace('|', ', ')}"
                  f"  [match {r['score'] * 100:.0f}%]")
        print()


if __name__ == "__main__":
    main()