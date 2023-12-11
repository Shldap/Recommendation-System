import imdb
import pandas as pd

# Create an instance of the IMDb class
ia = imdb.IMDb()

# Define a function to fetch movie details using IMDbPY
def get_movie_details(movie_id):
    movie = ia.get_movie(movie_id)
    title = movie.get('title', '')
    year = movie.get('year', '')
    rating = movie.get('rating', '')
    return title, year, rating

# Define a list of movie IDs
movie_ids = [1, 2, 3, 4, 5]  # Example movie IDs

# Fetch movie details and create a list of dictionaries
movies_data = []
for movie_id in movie_ids:
    title, year, rating = get_movie_details(movie_id)
    movies_data.append({'movieId': movie_id, 'title': title, 'year': year, 'rating': rating})

# Create a DataFrame with movie data
movies_df = pd.DataFrame(movies_data)

# Save the movies DataFrame to a CSV file
movies_df.to_csv('movies.csv', index=False)

# Generate random ratings for each user and movie
num_users = 100
ratings_data = []
for user_id in range(1, num_users + 1):
    for movie_id in movie_ids:
        rating = round(1 + (9 - 1) * (user_id / num_users), 1)  # Random rating between 1.0 to 9.0
        ratings_data.append({'userId': user_id, 'movieId': movie_id, 'rating': rating})

# Create a DataFrame with ratings data
ratings_df = pd.DataFrame(ratings_data)

# Save the ratings DataFrame to a CSV file
ratings_df.to_csv('ratings.csv', index=False)
