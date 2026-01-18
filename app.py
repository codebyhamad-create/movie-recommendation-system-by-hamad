import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/500"
    except:
        return "https://via.placeholder.com/500"

st.header('Movie Recommender System')

# Relative paths (Works on any computer)
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button('Show Recommendation'):
    index = movies[movies['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    cols = st.columns(5)
    for i in range(5):
        movie_id = movies.iloc[distances[i+1][0]].movie_id
        with cols[i]:
            st.text(movies.iloc[distances[i+1][0]].title)
            st.image(fetch_poster(movie_id))
