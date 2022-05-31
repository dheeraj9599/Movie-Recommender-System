<<<<<<< HEAD:Web App/web.py
# Here are the basic libraries for the basic operations
from unittest import result
import pandas as pd
import pickle
import requests

# for using Stickers and animations
from streamlit_lottie import st_lottie

# Streamlit is used for the Web UI
import streamlit as st


# from here I am fetching the posters
def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=4125b44e30d3b8c21db8d9bfaceddbfe&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']

    if poster_path == None :
        
        return "https://th.bing.com/th/id/R.e5e0354514c70fd464177625d85ad530?rik=2cpvKOckFETaUA&riu=http%3a%2f%2fdrpp-ny.org%2fwp-content%2fuploads%2f2014%2f07%2fsorry-image-not-available.png&ehk=Vr%2brN9GaGUkGM2yuKpT1w2pQfZ16Wq3tpZf3hCvrBbg%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1"
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def normal_recommendations(title,n):
    
    # index of movie title
    idx = indices[title]
    
    # finding similarity scores and sorting the resultant movies in descending order of sim_scores
    
    # enumerate function holds the indixes while calculating similarity
    sim_scores = list(enumerate(Matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    # here is the whole movie data required for applying average weighted technique 
    movie_req = Final_Movies_list.iloc[movie_indices][['id', 'title', 'genres', 'cast','overview', 'weigh_avg_rating','year']]
    
    return movie_req



# optimized_recommendations function
def optimized_recommendations(title, n):
    
    # index of movie title
    idx = indices[title]
    
    # finding similarity scores and sorting the resultant movies in descending order of sim_scores
    
    # enumerate function holds the indixes while calculating similarity
    sim_scores = list(enumerate(Matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    # here is the whole movie data required for applying average weighted technique 
    movie_req = Final_Movies_list.iloc[movie_indices][['id', 'title', 'genres', 'cast','overview', 'weigh_avg_rating','year']]
    
    
    result = movie_req.sort_values('weigh_avg_rating', ascending=False).head(n)
    
    return result
# # # # # # # # # # # end of the functions # # # # # # # # # #  # # #




# From here I am starting the reading

Final_Movies_list = pickle.load(open('New_data.pkl','rb'))
Matrix = pickle.load(open('matrix.pkl','rb'))


# Title of Movies
Title_list = Final_Movies_list['title'].values


# fetching indexes of movie titles
indices = pd.Series(Final_Movies_list.index, index = Final_Movies_list['title'])

#Stoting Top-rated movies 
Top_rated_movies = Final_Movies_list.sort_values('weigh_avg_rating', ascending=False).head(50)



st.set_page_config(page_title="Recommendation engine", page_icon=":movie_camera:", layout="wide")

# header section


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


hey = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_khzniaya.json")    
welcome = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_1TcivY.json")    
with st.container():
    st.write("---")
    l_col, r_col = st.columns(2)
    with l_col:
        st.subheader("Hi, I am Dheeraj :wave:")
        st.subheader("A Front-end Web Developer")
        st_lottie(welcome, height=150, key="Welcome" )
        st.header("To My Website of Movie Recommender System")
        

    with r_col:
        st_lottie(hey, height=300, key="Hello")    
st.write("---")

if __name__ == '__main__':

    st.header('Movie Recommender System') 
    Str = ['--------Select--------', 'Recommend similar Movies', 'Recommend similar Movies with high ratings','Recommend Top Rated Movies']   
    Str_options = st.selectbox('How may I recommend movies to you ?', Str)

    # recommending movies according to normal_recommendaion function

    if Str_options == Str[1]:
        movie_selected = st.selectbox('Please Select a Movie', Title_list)
        movie_count = st.slider("Select the Frequency",1,25,5)
        if st.button('Click here To Recommend'): 

            movie = Final_Movies_list[Final_Movies_list['title'] == movie_selected]

            st.subheader("You Selected This Movie")
            with st.container():
                index = movie.index[0]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

            with st.container():    
                with col1:
                    st.image(fetch_poster(movie['id'][index]), width = 150, caption = movie['title'][index])
                
                with col2:
                    st.write(movie['genres'][index])

                with col3:
                    st.write(movie['cast'][index])    

                with col4:
                    st.write(movie['overview'][index])        
            st.write("---")    



            st.subheader("Here are the Recommendations For you")
            st.subheader("Hope You like these movies")

            result = normal_recommendations(movie_selected, movie_count)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1

    # recommending movies according to optimized_recommendaion function
                   
    elif Str_options == Str[2]:
        movie_selected = st.selectbox('Please Select a Movie', Title_list)
        movie_count = st.slider("Select the Frequency",1,25,5)
        if st.button('Click here To Recommend'): 

            movie = Final_Movies_list[Final_Movies_list['title'] == movie_selected]

            st.subheader("You Selected This Movie")
            with st.container():
                index = movie.index[0]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

            with st.container():    
                with col1:
                    st.image(fetch_poster(movie['id'][index]), width = 150, caption = movie['title'][index])
                
                with col2:
                    st.write(movie['genres'][index])

                with col3:
                    st.write(movie['cast'][index])    

                with col4:
                    st.write(movie['overview'][index])        
            st.write("---")

            st.write("Hope You also like these movies")
            result = optimized_recommendations(movie_selected,movie_count)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1
    # recommending Top rated Movies
    elif Str_options == Str[3]:
        movie_count = st.slider("Select the Frequency",1,50,10)
        if st.button('Click here To Recommend'): 
            st.subheader("Here are the Recommendations For you")
            st.subheader("Hope You like these movies")
            result = Top_rated_movies
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1

    else:
        st.write('Please Select a option')

st.write("---")
st.title("Thank You For Visiting This Website :heart: :blue_heart: :purple_heart:")
=======
# Here are the basic libraries for the basic operations
from unittest import result
import pandas as pd
import pickle
import requests

# for using Stickers and animations
from streamlit_lottie import st_lottie

# Streamlit is used for the Web UI
import streamlit as st


# from here I am fetching the posters
def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=4125b44e30d3b8c21db8d9bfaceddbfe&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']

    if poster_path == None :
        
        return "https://th.bing.com/th/id/R.e5e0354514c70fd464177625d85ad530?rik=2cpvKOckFETaUA&riu=http%3a%2f%2fdrpp-ny.org%2fwp-content%2fuploads%2f2014%2f07%2fsorry-image-not-available.png&ehk=Vr%2brN9GaGUkGM2yuKpT1w2pQfZ16Wq3tpZf3hCvrBbg%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1"
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def normal_recommendations(title,n):
    
    # index of movie title
    idx = indices[title]
    
    # finding similarity scores and sorting the resultant movies in descending order of sim_scores
    
    # enumerate function holds the indixes while calculating similarity
    sim_scores = list(enumerate(Matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    # here is the whole movie data required for applying average weighted technique 
    movie_req = Final_Movies_list.iloc[movie_indices][['id', 'title', 'genres', 'cast','overview', 'weigh_avg_rating','year']]
    
    return movie_req



# optimized_recommendations function
def optimized_recommendations(title, n):
    
    # index of movie title
    idx = indices[title]
    
    # finding similarity scores and sorting the resultant movies in descending order of sim_scores
    
    # enumerate function holds the indixes while calculating similarity
    sim_scores = list(enumerate(Matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    # here is the whole movie data required for applying average weighted technique 
    movie_req = Final_Movies_list.iloc[movie_indices][['id', 'title', 'genres', 'cast','overview', 'weigh_avg_rating','year']]
    
    
    result = movie_req.sort_values('weigh_avg_rating', ascending=False).head(n)
    
    return result
# # # # # # # # # # # end of the functions # # # # # # # # # #  # # #




# From here I am starting the reading

Final_Movies_list = pickle.load(open('New_data.pkl','rb'))
Matrix = pickle.load(open('matrix.pkl','rb'))


# Title of Movies
Title_list = Final_Movies_list['title'].values


# fetching indexes of movie titles
indices = pd.Series(Final_Movies_list.index, index = Final_Movies_list['title'])

#Stoting Top-rated movies 
Top_rated_movies = Final_Movies_list.sort_values('weigh_avg_rating', ascending=False).head(50)



st.set_page_config(page_title="Recommendation engine", page_icon=":movie_camera:", layout="wide")

# header section


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


hey = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_khzniaya.json")    
welcome = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_1TcivY.json")    
with st.container():
    st.write("---")
    l_col, r_col = st.columns(2)
    with l_col:
        st.subheader("Hi, I am Dheeraj :wave:")
        st.subheader("A Front-end Web Developer")
        st_lottie(welcome, height=150, key="Welcome" )
        st.header("To My Website of Movie Recommender System")
        

    with r_col:
        st_lottie(hey, height=300, key="Hello")    
st.write("---")

if __name__ == '__main__':

    st.header('Movie Recommender System') 
    Str = ['--------Select--------', 'Recommend similar Movies', 'Recommend similar Movies with high ratings','Recommend Top Rated Movies']   
    Str_options = st.selectbox('How may I recommend movies to you ?', Str)

    # recommending movies according to normal_recommendaion function

    if Str_options == Str[1]:
        movie_selected = st.selectbox('Please Select a Movie', Title_list)
        movie_count = st.slider("Select the Frequency",1,25,5)
        if st.button('Click here To Recommend'): 

            movie = Final_Movies_list[Final_Movies_list['title'] == movie_selected]

            st.subheader("You Selected This Movie")
            with st.container():
                index = movie.index[0]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

            with st.container():    
                with col1:
                    st.image(fetch_poster(movie['id'][index]), width = 150, caption = movie['title'][index])
                
                with col2:
                    st.write(movie['genres'][index])

                with col3:
                    st.write(movie['cast'][index])    

                with col4:
                    st.write(movie['overview'][index])        
            st.write("---")    



            st.subheader("Here are the Recommendations For you")
            st.subheader("Hope You like these movies")

            result = normal_recommendations(movie_selected, movie_count)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1

    # recommending movies according to optimized_recommendaion function
                   
    elif Str_options == Str[2]:
        movie_selected = st.selectbox('Please Select a Movie', Title_list)
        movie_count = st.slider("Select the Frequency",1,25,5)
        if st.button('Click here To Recommend'): 

            movie = Final_Movies_list[Final_Movies_list['title'] == movie_selected]

            st.subheader("You Selected This Movie")
            with st.container():
                index = movie.index[0]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

            with st.container():    
                with col1:
                    st.image(fetch_poster(movie['id'][index]), width = 150, caption = movie['title'][index])
                
                with col2:
                    st.write(movie['genres'][index])

                with col3:
                    st.write(movie['cast'][index])    

                with col4:
                    st.write(movie['overview'][index])        
            st.write("---")

            st.write("Hope You also like these movies")
            result = optimized_recommendations(movie_selected,movie_count)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1
    # recommending Top rated Movies
    elif Str_options == Str[3]:
        movie_count = st.slider("Select the Frequency",1,50,10)
        if st.button('Click here To Recommend'): 
            st.subheader("Here are the Recommendations For you")
            st.subheader("Hope You like these movies")
            result = Top_rated_movies
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.subheader("[TITLE]")
                with col2:
                    st.subheader("[GENRE]")
                with col3:
                    st.subheader("[CAST]")

                with col4:
                    st.subheader("[OVERVIEW]")    

                title = []
                poster = []
                Cast = []
                gen_List = []
                ovw_List = []      
                i = 0
                while i<movie_count :
                    idx = result.iloc[i].id
                    poster.append(fetch_poster(idx))
                    title.append(result.iloc[i].title)
                    Cast.append(result.iloc[i].cast)
                    gen_List.append(result.iloc[i].genres)
                    ovw_List.append(result.iloc[i].overview)
 
                    st.write("---")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.image(poster[i], width = 150, caption = title[i])
                
                    with col2:
                        st.write(gen_List[i])

                    with col3:
                        st.write(Cast[i])    

                    with col4:
                        st.write(ovw_List[i])        
                    i += 1

    else:
        st.write('Please Select a option')

st.write("---")
st.title("Thank You For Visiting This Website :heart: :blue_heart: :purple_heart:")
>>>>>>> e7499e5df7bf1a9781d5fb9b19e5607185be5308:web.py
