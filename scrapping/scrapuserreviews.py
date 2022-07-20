import pandas as pd
from sqlalchemy import asc
from sympy import mobius

item_similiary_df = []


def get_similiar_movs(movie_name, user_rating):
    similiar_score = item_similiary_df[movie_name]*(user_rating-2.5)
    similiar_score = similiar_score.sort_values(ascending=False)
    return similiar_score


def collab_filter(favMovies):

    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')

    ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)

    # making rows userid, coloumns movie id, values=rating

    user_ratings = ratings.pivot_table(index=['userId'], columns=[
        'title'], values='rating')

    # removing Nans, by removing movies with less than 10 ratings
    user_ratings = user_ratings.dropna(thresh=10, axis=1).fillna(0)

    # using inbuilt pierson correlation
    item_similiary_df = user_ratings.corr(
        method='pearson')  # the similiary matrix

    #favMovies = [("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)", 5)]

    similiar_movies = pd.DataFrame()

    for movie, rating in favMovies:
        similiar_movies = similiar_movies.append(
            get_similiar_movs(movie, rating), ignore_index=True)

    similiar_movies.sum().sort_values(ascending=False)

    return similiar_movies
