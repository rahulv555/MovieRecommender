import functools as ft
from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

###### helper functions. Use them when needed #######


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]
##################################################

# Step 1: Read CSV File into dataframe
# df = pd.read_csv("movie_dataset.csv")
# rint(df.columns)


with open("content_based.json", encoding="utf8") as f:
    data = literal_eval(f.read())
i = 0
for d in data:
    d['index'] = i
    i += 1

# print(data)
dfdesc = pd.json_normalize(data)
# df.set_index('i', inplace=True)

###################################################################
with open("titlegenre.json", encoding="utf8") as f:
    data = literal_eval(f.read())
i = 0
for d in data:
    d['index'] = i
    i += 1
dftitgen = pd.json_normalize(data)


########################################################################
with open("tags.json", encoding="utf8") as f:
    data = literal_eval(f.read())
i = 0
for d in data:
    d['index'] = i
    i += 1
dftags = pd.json_normalize(data)


# JOINING THE DFS
dfs = [dfdesc, dftitgen, dftags]


df = pd.merge(dfdesc, dftitgen, on='id')
df = pd.merge(df, dftags)
print(df)


def content_rec(fav_movie):
    ##################################################
    # Step 2: Select Features
    features = ['tags', 'genres', 'title', 'description']

    for feature in features:
        df[feature] = df[feature].fillna('')  # fill all NaN with empty string

    ##################################################
    # Step 3: Create a column in DF which combines all selected features

    def combine_features(row):  # take a row from the dataset
        s = " "
        # print(s.join(row["genres"]))
        return row['tags']+" "+row['title']+' '+row["description"]+" "+s.join(row["genres"])

    # creating new column in the df
    # applies the function on the df vertically(pass each row individually)
    df["combined_features"] = df.apply(combine_features, axis=1)

    ##################################################

    # Step 4: Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    # for each word in the combined features of each row, we find the count(occurence) of each word in that row

    ##################################################

    # Step 5: Compute the Cosine Similarity based on the count_matrix

    # gives the similiarity scores between all the movies
    cosine_sim = cosine_similarity(count_matrix)
    # each row  represents one movie, and the columns contain the similiarity with the other movies

    ##################################################
    # INPUT MOVIE FROM USER
    movie_user_likes = fav_movie

    ##################################################
    # Step 6: Get index of this movie from its title
    movie_index = get_index_from_title(movie_user_likes)

    # gives list of (tuples) in the form [(index of movie, similiarity score)]
    similiar_movies = list(enumerate(cosine_sim[movie_index]))

    ##################################################
    # Step 7: Get a list of similar movies in descending order of similarity score
    # sorting

    sorted_similiar_movies = sorted(
        similiar_movies, key=lambda x: x[1], reverse=True)

    ##################################################
    # Step 8: Print titles of first 50 movies

    i = 0

    sorted_similiar_movies_tuples = []

    for movie in sorted_similiar_movies:
        sorted_similiar_movies_tuples.append(
            (get_title_from_index(movie[0]), movie[0]))
        i = i+1
        if(i > 50):
            break

    return sorted_similiar_movies_tuples


#print(content_rec("The Godfather"))
