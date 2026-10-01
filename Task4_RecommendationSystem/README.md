# Task 4: Recommendation System

A movie recommendation system using **content-based filtering**. It suggests
movies similar to the ones you like, or movies that match a short text
description you type.

## Features
- Pick one or more movies you liked and get similar movies
- Or describe what you want ("space survival", "friends on a road trip")
- Optional genre filter and adjustable number of results
- Match percentage for every recommendation
- Streamlit web UI and a terminal version
- Included dataset of 96 movies (Hollywood, animation and Bollywood), so
  nothing needs to be downloaded

## How it works
1. Each movie is turned into text: its genres (repeated so they weigh more) plus a short plot description.
2. **TF-IDF** converts that text into a vector, giving higher weight to distinctive words.
3. **Cosine similarity** measures how close two movie vectors are.
4. For several liked movies, the similarity scores are averaged, then the top matches are shown (the liked movies themselves are excluded).

## Project structure
```
recommender.py     # TF-IDF + cosine similarity engine, terminal version
app.py             # Streamlit web UI
movies.csv         # dataset: title, year, genres, description
requirements.txt
```

## Run
```
pip install -r requirements.txt
streamlit run app.py
```
Or in the terminal:
```
python recommender.py
```

## Using your own data
Replace `movies.csv` with any file that has the columns
`title, year, genres, description` (genres separated by `|`), for example a
prepared MovieLens or TMDB export.