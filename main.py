import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk

# Load the movie dataset
movies = pd.read_csv('movies.csv')  # Assuming you have a CSV file with movie data

# Load the ratings dataset
ratings = pd.read_csv('ratings.csv')  # Assuming you have a CSV file with ratings data

# Merge movies and ratings based on movieId
movie_ratings = pd.merge(movies, ratings, on='movieId')

# Create a pivot table with user ratings for each movie
pivot_table = movie_ratings.pivot_table(index='userId', columns='title', values='rating')

# Calculate the similarity matrix using cosine similarity
similarity_matrix = pd.DataFrame(cosine_similarity(pivot_table.fillna(0)), index=pivot_table.index, columns=pivot_table.index)

# Collaborative filtering recommendation
def collaborative_filtering(user_id, num_recommendations):
    user_ratings = pivot_table.loc[user_id]
    similar_users = similarity_matrix[user_id].sort_values(ascending=False)[1:]  # Exclude the user itself
    similar_users_ratings = pivot_table.loc[similar_users.index]
    predicted_ratings = similar_users_ratings.mean().sort_values(ascending=False)
    recommendations = predicted_ratings.drop(user_ratings.dropna().index)
    return recommendations[:num_recommendations].index

# Content-based filtering recommendation
def content_based_filtering(movie_title, num_recommendations):
    movie_features = pivot_table.columns
    movie_idx = movie_features.get_loc(movie_title)
    similarities = cosine_similarity(pivot_table.iloc[:, movie_idx].values.reshape(1, -1), pivot_table.values)
    similar_movies_indices = np.argsort(similarities)[0][::-1][1:]  # Exclude the movie itself
    recommendations = pivot_table.columns[similar_movies_indices]
    return recommendations[:num_recommendations]

# GUI using Tkinter
def recommend_movies():
    user_id = int(user_entry.get())
    movie_title = movie_entry.get()
    num_recommendations = int(num_entry.get())
    cf_recommendations = collaborative_filtering(user_id, num_recommendations)
    cbf_recommendations = content_based_filtering(movie_title, num_recommendations)
    cf_output.config(text="Collaborative Filtering:\n" + "\n".join(cf_recommendations))
    cbf_output.config(text="Content-Based Filtering:\n" + "\n".join(cbf_recommendations))

# Create the GUI
root = tk.Tk()

user_label = tk.Label(root, text="User ID:")
user_label.pack()
user_entry = tk.Entry(root)
user_entry.pack()

movie_label = tk.Label(root, text="Movie Title:")
movie_label.pack()
movie_entry = tk.Entry(root)
movie_entry.pack()

num_label = tk.Label(root, text="Number of Recommendations:")
num_label.pack()
num_entry = tk.Entry(root)
num_entry.pack()

recommend_button = tk.Button(root, text="Recommend Movies", command=recommend_movies)
recommend_button.pack()

cf_output = tk.Label(root)
cf_output.pack()

cbf_output = tk.Label(root)
cbf_output.pack()

root.mainloop()
