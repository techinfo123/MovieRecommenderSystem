import pickle
import streamlit as st
import requests
import lzma  

# Fetch poster from TMDB
def fetch_poster(movie_id):
    """Fetches the movie poster URL from TMDB"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return ""  # Return an empty string if no poster is found
    except requests.exceptions.RequestException as e:
        st.warning(f"Failed to fetch poster for movie {movie_id}: {e}")
        return ""  # Return empty string if request fails

# Recommendation function
def recommend(movie):
    """Recommends 5 similar movies based on the selected movie"""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('🎬 Movie Recommender System')

# Load data
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    with lzma.open('similarity.pkl.xz', 'rb') as f:  # Using lzma for .xz compressed file
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"Error loading data files: {e}")

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Display recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Create columns dynamically based on the 5 recommended movies
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            if recommended_movie_posters[i]:
                st.image(recommended_movie_posters[i], use_container_width=True)
            else:
                st.text("No Poster Available")
