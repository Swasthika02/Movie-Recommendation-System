
import pickle
import streamlit as st
import requests

st.header("Movie Recommendation System using Machine Learning")
movies = pickle.load(open('Artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('Artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get a recommendation',
    movie_list
)

#def fetch_poster(movie_id):
    
    #api_key = '187675e25cd464074f6961131a8d3620'

    #url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    #data = requests.get(url)
    #data = data.json()
    #poster_path = data['poster_path']
    #full_path = "https://image.tmdb.org/t/p/" + poster_path
    #return full_path
import requests

def fetch_poster(movie_id):

    api_key = "5de56ca690374c0c731cfb9dd224b436"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"TMDB Error: {response.status_code} for movie_id = {movie_id}")
            return ""

        data = response.json()
        print(data)

        poster_path = data.get('poster_path')
        print("Movie ID:", movie_id)
        print("Poster Path:", data.get("poster_path"))

        if poster_path is None:
            print(f"No poster found for movie_id = {movie_id}")
            return ""

        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"

        return full_path

    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        return ""

    except Exception as e:
        print("Error:", e)
        return ""
 

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:20]:

        movie_id = movies.iloc[i[0]]['movie_id']

        poster = fetch_poster(movie_id)

        if poster:
            recommended_movies_name.append(
            movies.iloc[i[0]]['title']
        )

            recommended_movies_poster.append(
            poster
        )

        if len(recommended_movies_name) == 5:
            break


    return recommended_movies_name, recommended_movies_poster

def display_movie(title, poster):
    st.markdown(
        f"""
        <div style="
            height:80px;
            text-align:center;
            font-weight:bold;
            overflow:hidden;
        ">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        poster,
        use_container_width=True
    )


if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        display_movie(
            recommended_movies_name[0],
            recommended_movies_poster[0]
        )

    with col2:
        display_movie(
            recommended_movies_name[1],
            recommended_movies_poster[1]
        )

    with col3:
        display_movie(
            recommended_movies_name[2],
            recommended_movies_poster[2]
        )

    with col4:
        display_movie(
            recommended_movies_name[3],
            recommended_movies_poster[3]
        )

    with col5:
        display_movie(
            recommended_movies_name[4],
            recommended_movies_poster[4]
        )