from ctypes import sizeof
import json
from selenium import webdriver
from time import sleep
from joblib import PrintTime
import requests
import html5lib
from bs4 import BeautifulSoup
import csv
import lxml


urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250",
        "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"]
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


def Scrape(url, headers):
    # r now has the raw HTML content
    r = requests.get(url=url, headers=headers)
    # print(r.content)

    # the raw content, and the parser
    soup = BeautifulSoup(r.content, 'html.parser')

    movies = []

    content = soup.find('tbody', attrs={'class': 'lister-list'})
    rows = content.find_all('tr')

    # iterating through each div containg a movies title
    for element in rows:
        title = element.find('td', attrs={'class': 'titleColumn'})
        post = {}
        post['title'] = title.a.text
        post['URL'] = title.a['href']
        movies.append(post)

    return movies


movies = []
for url in urls:
    movies = movies + Scrape(url, headers)


# TILL NOW, SCRAPPED MOVIE TITLE AND URL in movies
#########################


moviesList = []
for mov in movies:
    movie = {}
    if(len(list(filter(lambda movie: movie['title'] == 'title', moviesList))) > 0):
        continue
    movie['title'] = mov['title']

    # extracting id
    movie['id'] = mov['URL'][7:16]
    # print(newm.id)
    moviesList.append(movie)

print(moviesList)

###########################################
# extracting description


def extractDesc(url):
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


def extractKeywords(url):
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


def extractGenre(url):
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


def extractDir(url):
    try:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        content = soup.find('tbody')
        director = content.find('a')
        director = director.text
        return director
    except:
        return ""


# extracting description and keywords
i = 1
for mov in moviesList:
    print(i)
    i += 1
    id = mov['id']
    urld = 'https://www.imdb.com/title/'+id+'/'
    urlk = 'https://www.imdb.com/title/'+id+'/keywords?ref_=tt_stry_kw'
    urlg = 'https://www.imdb.com/title/'+id+'/'
    urldr = 'https://www.imdb.com/title/'+id+'/fullcredits?ref_=tt_cl_sm'

    mov['description'] = extractDesc(urld)
    mov['keywords'] = extractKeywords(urlk)
    #mov['genre'] = extractGenre(urlg)
    mov['director'] = extractDir(urldr)


# print(moviesList)

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
