# Movie-Recommendation-Engine
I made 3 Types of Recommendation Engine 

# 1.Simple Recommemder System Model : In this model I used TMDB 5000 Movie dataset : https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata which contains movies.csv and credits.csv.

IMPORTANT LIBRARIES USED :

for data analysis:
import matplotlib.pyplot as plt
import seaborn as sns

for scaledown the values:
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

In this Model I used Weighted average rating and some statistical approach to recommend movies on the basis of Weight average ratings
whose formula is given by 
                      
# Average_weighted_Technique
From this technique we are going to calculate the average weighted rating whose formula is given by : 
W = (R*v + C*m)/ v + m 
R is the average rating of the movie
C is the mean of votes w.r.t all the movies
v is the number of votes w.r.t each movie(vote_count)
m is the minimum votes required to be in a list Top movies 

Using the average_weighted_technique I sorted the movies and give recommendations. Then I used both weighted_average_rating and popularity score giving 50%-50% priority to both and recommend popular high rated movies. then I pickle the 

# 2. Content-Based-Recommendation-engine : In this model I Used the same dataset by pickling dataset from 1st recommender System model as we need average weighted ratings in furthure process.

IMPORTANT LIBRARIES REQUIRED: scikit-surprise, 
Approaches used : 1. Preprocessing of data(duplicates, missing values, unnecessary columns, merging, modifying)
                  2. Vectorization
                  3. Cosine similarity
                  4. Optimizing using weighted average ratings
In this model I first do preprocessing of dataset like finding duplicates, missing values and dropping the unnecessary columns, after that i cleaned the required columns for checking similarities between genres, cast, crew, keywords as it is a content based system. then I merged all this columns to make a final details columns and then convert it into the vectors of strings and then check the similarity scores between each movie and recommend movies with high similarity.

# 3. Collaborative filtering : In this model I used movie_meta.csv dataset as it contains users with ratings. In this model I filtered the movies on the basis of no. of user ratings and minnimu no. of ratings required(threshold rating).

Approches used : 1. Statistical Filtering
                 2. Pivot Table
                 3. Correlation
                 4.KNN algorithm 
NOTE : Run The Collaborative_Filtering(SVD and KNN) ipynb file on google collab.             
