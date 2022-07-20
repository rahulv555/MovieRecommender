import json
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
df = pd.DataFrame()

for f in range(4, 101):
    print(f)
    url = "https://www.imdb.com/list/ls057823854/?st_dt=&mode=detail&page=" + \
        str(f)+"&sort=release_date,desc"
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = html_soup.find_all(
        'div', class_='lister-item mode-detail')
    names = []
    years = []
    imdb_ratings = []
    metascores = []
    votes = []
    plots = []
    genre = []
    lengths = []
    collections = []
    starss = []
    directors = []
    urls = []

    for container in movie_containers:

        if container.find('div', class_='ratings-metascore') is not None or None:
            name = container.h3.a.text
            names.append(name)

            imdb = container.find(
                'span', class_='ipl-rating-star__rating').text
            imdb_ratings.append(imdb)

            year = container.h3.find(
                'span', class_='lister-item-year').text
            years.append(year)

            url = container.find(
                'h3', class_='lister-item-header').find('a')['href']
            url = url[7:]
            urls.append(url)
            # print(url)

            m_score = container.find('span', class_='metascore').text
            metascores.append(int(m_score))

            b = container.find_all('span', attrs={'name': 'nv'})
            vote = b[0].text
            votes.append(vote)

            if len(b) == 2:
                collection = b[1].text
                collections.append(collection)

            else:
                collections.append('0')

            par = container.find_all('p')
            length = par[0].find('span', class_='genre').text
            genre.append(length)

            length = par[0].find('span', class_='runtime').text
            lengths.append(length)

            plot = par[1].text
            plots.append(plot)
            # print(plot)
            stars_director = container.find_all('p')[2].text
            directors.append(stars_director)

    test_df = pd.DataFrame({'movie': names,
                            'imdiid': urls,
                            'year': years,
                            'imdb': imdb_ratings,
                            'metascore': metascores,
                            'votes': votes,
                            'Plot': plots,
                            'genre': genre,
                            'duration': lengths,
                            "revenue": collections,
                            "directors": directors
                            })

    df = pd.concat([df, test_df])

    # print(df)

    if f % 10 == 0:
        df.to_csv(str(f)+"page.csv")

# with open("moredata.json", "w") as final:
#     json.dump(df.to_json, final)
