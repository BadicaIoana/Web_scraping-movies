import requests
import csv
from bs4 import BeautifulSoup

def get_movies(max_number_of_pages):
    # Open a file in write mode and create a CSV writer object
    with open('movies.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['title', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the headers to the CSV file
        writer.writeheader()

        # Loop through the specified number of pages
        page = 1
        while page <= max_number_of_pages:
            # Construct the URL for the current page
            url = 'https://www.cinemagia.ro/filme/?&pn=' + str(page)

            # Send a GET request to the URL and parse the HTML response
            source_code = requests.get(url)
            soup = BeautifulSoup(source_code.content)

            # Find all the div elements that contain movie titles
            movies_title_div = soup.find_all('div', {'class':'title'})

            # Extract the movie titles from the div elements
            movies = [movie.text.strip('\n')[0:movie.text.strip('\n').find('\n')] for movie in movies_title_div]
            
            # Remove the last element, which is not a movie title
            movies.remove(movies[-1])

            # Find all the div elements that contain IMDb ratings
            rating_div = soup.find_all('div',{'class':'rating'})

            # Extract the IMDb ratings from the div elements
            rating_imdb = [float(rating.text.strip('\n')[rating.text.strip('\n').find(' ') + 1:]) for rating in rating_div]

            # For each movie with a rating of 8 or above, write the title and rating to the CSV file
            for i in range(len(movies)):
                if rating_imdb[i] >= 8:
                    writer.writerow({'title': movies[i], 'rating': rating_imdb[i]})
            
            # Go to the next page
            page += 1

# Call the `get_movies` function with the number of pages as the argument
if __name__ == '__main__':
    get_movies(100)

