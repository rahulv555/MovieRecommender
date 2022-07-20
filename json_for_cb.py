import pandas as pd
import json


moviesList = []

with open('./json/mydata1000.json', 'r', encoding="utf-8") as f:
    data = json.load(f)
    moviesList += data


for i in range(2, 10):
    with open('./json/mydata'+str(i)+'000.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        moviesList += data


with open('./json/mydata9740.json', 'r', encoding="utf-8") as f:
    data = json.load(f)
    moviesList += data

for movie in moviesList:
    movie["id"]=int(movie["id"])

print(len(moviesList))

with open("content_based.json", "w", encoding="utf-8") as final:
    json.dump(moviesList, final)



