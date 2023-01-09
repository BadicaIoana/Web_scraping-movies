import requests
import csv
from bs4 import BeautifulSoup

def get_movies(max_number_of_pages):
    with open('movies.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['title', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        page = 1
        while page <= max_number_of_pages:
            url = 'https://www.cinemagia.ro/filme/?&pn=' + str(page)
            source_code = requests.get(url)
            soup = BeautifulSoup(source_code.content)
            movies_title_div = soup.find_all('div', {'class':'title'})
            movies = [movie.text.strip('\n')[0:movie.text.strip('\n').find('\n')] for movie in movies_title_div]
            movies.remove(movies[-1])
            rating_div = soup.find_all('div',{'class':'rating'})
            rating_imdb = [float(rating.text.strip('\n')[rating.text.strip('\n').find(' ') + 1:]) for rating in rating_div]

            for i in range(len(movies)):
                if rating_imdb[i] >= 8:
                    writer.writerow({'title': movies[i], 'rating': rating_imdb[i]})
            page += 1

if __name__ == '__main__':
    get_movies(100)
