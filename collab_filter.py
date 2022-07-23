import pandas as pd


item_similiary_df = []


def get_similiar_movs(movie_id, user_rating):
    similiar_score = item_similiary_df[movie_id]*(user_rating-2.5)
    similiar_score = similiar_score.sort_values(ascending=False)
    return similiar_score


def collab_filter(favMovies):

    tempMovies = []
    for movie in favMovies:
        tempMovies.append((movie[1], movie[2]))

    favMovies = tempMovies

    ratings = pd.read_csv('ratings.csv')
    movies = pd.read_csv('movies.csv')

    ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)

    ratings = ratings[ratings.movieId <= 9740]
    movies = movies[movies.movieId <= 9740]

    # making rows userid, coloumns movie id, values=rating

    user_ratings = ratings.pivot_table(index=['userId'], columns=[
        'movieId'], values='rating')

    # removing Nans, by removing movies with less than 10 ratings
    user_ratings = user_ratings.dropna(thresh=10, axis=1).fillna(0)

    # using inbuilt pierson correlation
    global item_similiary_df
    item_similiary_df = user_ratings.corr(
        method='pearson')  # the similiary matrix

    print(item_similiary_df)


    #favMovies = [("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)", 5)]

    similiar_movies = pd.DataFrame()

    for movieId, rating in favMovies:
        similiar_movies = similiar_movies.append(
            get_similiar_movs(movieId, rating), ignore_index=True)

    similiar_movies.sum().sort_values(ascending=False)
    print(similiar_movies)

    return similiar_movies
