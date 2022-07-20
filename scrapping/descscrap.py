from ctypes import sizeof
import json
from types import SimpleNamespace
from selenium import webdriver
from time import sleep
from joblib import PrintTime
import requests
import html5lib
from bs4 import BeautifulSoup
import csv
import lxml
import pandas as pd


urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250",
        "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"]
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


# def Scrape(url, headers):
#     # r now has the raw HTML content
#     r = requests.get(url=url, headers=headers)
#     # print(r.content)

#     # the raw content, and the parser
#     soup = BeautifulSoup(r.content, 'html.parser')

#     movies = []

#     content = soup.find('tbody', attrs={'class': 'lister-list'})
#     rows = content.find_all('tr')

#     # iterating through each div containg a movies title
#     for element in rows:
#         title = element.find('td', attrs={'class': 'titleColumn'})
#         post = {}
#         post['title'] = title.a.text
#         post['URL'] = title.a['href']
#         movies.append(post)

#     return movies


# movies = []
# for url in urls:
#     movies = movies + Scrape(url, headers)


# # TILL NOW, SCRAPPED MOVIE TITLE AND URL in movies
# #########################


# moviesList = []
# for mov in movies:
#     movie = {}
#     if(len(list(filter(lambda movie: movie['title'] == 'title', moviesList))) > 0):
#         continue
#     movie['title'] = mov['title']

#     # extracting id
#     movie['id'] = mov['URL'][7:16]
#     # print(newm.id)
#     moviesList.append(movie)

# print(moviesList)

###########################################
# extracting description


def extractDescIMDB(url):
    try:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        contentdesc = soup.find('div', attrs={'class': 'sc-16ede01-7 hrgVKw'})
        contentdesc = contentdesc.find(
            'span', attrs={'class': 'sc-16ede01-0 fMPjMP'})
        # print(contentdesc.text)
        return contentdesc.text
    except:
        return ""


def extractKeywordsIMDB(url):
    try:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        keywords = ""

        content = soup.find('tbody')
        rows = content.find_all('td', attrs={'class': 'soda sodavote'})
        for row in rows:
            keywords = keywords + row['data-item-keyword'] + " "
        # print(keywords)
        return keywords
    except:
        return ""


def extractGenreIMDB(url):
    try:
        browser = webdriver.Chrome('chromedriver.exe')
        browser.get(url)
        sleep(10)
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')

        genre = soup.find('li', attrs={'data-testid': 'storyline-genres'})
        genre = genre.find('a', attrs={
            'class': 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
        genre = genre['href'][22:]
        s = ""
        for g in genre:
            if g == '&':
                break
            s = s+g
        genre = s
        browser.close()
        return genre
    except:
        return ""


def extractDirIMDB(url):
    try:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        content = soup.find('tbody')
        director = content.find('a')
        director = director.text
        return director
    except:
        return ""


def extractDesc(url):
    try:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        contentdesc = soup.find('div', attrs={'class': 'overview'})
        contentdesc = contentdesc.find(
            'p')
        # print(contentdesc.text)
        return contentdesc.text
    except:
        return ""


movies = pd.read_csv('links.csv')
# print(movies['imdbId'])
moviesId = movies['tmdbId']


moviesList = []  # FINAL LIST OF MOVIE OBJECTS


# extracting description and keywords
i = 0
# for id in moviesId:
for i in range(9741, 10000):
    movie = {}
    id = moviesId[i]
    print(i)
    i += 1
    id = str(id)
    movie["id"] = str(i)
    movie["tmdbid"] = id
    urld = 'https://www.themoviedb.org/movie/'+id
    # urlk = 'https://www.imdb.com/title/'+id+'/keywords?ref_=tt_stry_kw'
    # urlg = 'https://www.imdb.com/title/'+id+'/'
    #urldr = 'https://www.themoviedb.org/movie/'+id
    # urlt = 'https://www.imdb.com/title/'+id+'/'

    movie['description'] = extractDesc(urld)
    # mov['keywords'] = extractKeywords(urlk)
    #mov['genre'] = extractGenre(urlg)
    #movie['director'] = extractDir(urldr)
    # movie['title']

    moviesList.append(movie)
    if i % 10 == 0:
        with open("mydata.json", "w") as final:
            json.dump(moviesList, final)

    if(i == 1000):
        break


# extracing title and genres
# i = 1


# for i in range(1, 9741):
#     moviesList.append({'id':i})


# movies = pd.read_csv('movies.csv')
# # print(movies['imdbId'])
# moviestitle = movies['title']
# moviesgenre = movies['genres']


# i = 0
# for movie in moviestitle:
#     moviesList[i]['title']= movie
#     i += 1
#     if(i==9740):
#         break


# i = 0
# for movie in moviesgenre:
#     moviesList[i]['genres'] = movie.split("|")
#     i += 1
#     if(i==9740):
#         break


# # FOR KEYWORDS (TAGS)
# movietags = pd.read_csv("tags.csv")


# for index, row in movietags.iterrows():
#     if 1<=int(row['movieId']) <= 9740:
#         if moviesList[row['movieId']]['tags']:
#             moviesList[row['movieId']]['tags'] = moviesList[row['movieId']
#                                                     ]['tags'] + " " + row['tag']
#         else:
#           moviesList[row['movieId']]['tags'] =row['tag']


print(moviesList)

# # writing this to a csv file
# filename = 'youtubevideos.csv'
# with open(filename, 'w', newline='\n', ) as f:
#     w = csv.DictWriter(f, ['title', 'URL'])
#     w.writeheader()
#     for post in movies:
#         w.writerow(post)
#         # print(post)

with open("mydata.json", "w") as final:
    json.dump(moviesList, final)
