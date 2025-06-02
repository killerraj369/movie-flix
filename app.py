import numpy as np
import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("api_key")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity_scores = np.load("similarities_compressed.npz")["similarities"]

def fetch_image(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w185/{poster_path}"
    return "https://via.placeholder.com/185x278.png?text=No+Image"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    similarity_score = similarity_scores[index]
    similar_movies = sorted(list(enumerate(similarity_score)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    for i in similar_movies:
        movie_id = movies.iloc[i[0]]['id']
        title = movies.iloc[i[0]]['title']
        poster = fetch_image(movie_id)
        link = f"https://www.themoviedb.org/movie/{movie_id}"
        recommendations.append([title, poster, link])
    return recommendations


# --- App UI ---
st.title('MovieFlix - The Movie Recommender🍿')
selected_movie = st.selectbox('Search a Movie You Like:', movies['title'].values)

if st.button('🔍 Recommend'):
    with st.spinner('Finding awesome recommendations... 🎬'):
        recs = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        title, poster, link = recs[idx]
        col.markdown(
            f"<a href='{link}' target='_blank' style='text-decoration:none; color:white; font-weight:bold;'>{title}</a>",
            unsafe_allow_html=True)
        col.image(poster, use_container_width=True)

