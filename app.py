# Här importeras Flask och request samt config-filen där API-nycklar finns.
from flask import Flask, render_template, request
import requests
import config

# Här skapas en instans.
app = Flask(__name__)

# Här skapas varibler för API-nycklar.
OMDB_API_KEY = config.OMDB_API_KEY
GOOGLE_BOOKS_API_KEY = config.GOOGLE_BOOKS_API_KEY

# Här berättar vi var appen ska hitta templates för programmet.
app.template_folder = "templates"

# Vi definierar en rutt och vad den rutten gör.
@app.route('/', methods=['GET', 'POST'])
def index():
    movie_data = None

    if request.method == 'POST':
        user_input = request.form.get('user_input')

        if user_input:
            try:
                movie_data = get_movie_data(user_input)

                if movie_data:
                    book_recommendations = get_book_recommendations(movie_data)
                    return render_template('index.html', movie=movie_data, books=book_recommendations)
                else:
                    return render_template('index.html', error='The movie was not found. Please try again.')
            except requests.exceptions.RequestException as e:
                print(f"Error fetching movie data: {e}")
                return render_template('index.html', error='An error occurred while fetching movie data.')

    return render_template('index.html', movie=movie_data)


# Funktion hämtar datan från filmnamnet via OMDB:s API.
def get_movie_data(movie_title):
    try:
        omdb_url = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}&plot=full'
        response = requests.get(omdb_url)
        response.raise_for_status()

# Datan vi får kommer in som Json och utifrån den datan gör vi ett urval vilka data vi vill visa.
        data = response.json()

        if data.get('Response') == 'True':
            return {
                'Title': data['Title'],
                'Year': data['Year'],
                'Plot': data['Plot'],
                'Actors': data['Actors'],
                'Ratings': data['imdbRating'],
                'Directors': data['Director'],
                'Poster': data['Poster'],
            }
    except requests.exceptions.RequestException as e:
        print(f"Error with OMDb API request: {e}")
    
    return None

# I denna funktion skickar vi med datan från filmen och får således ut respons från Google Books API som har koppling till informationen som hör till filmen.
def get_book_recommendations(movie_data):
    try:
        google_books_url = 'https://www.googleapis.com/books/v1/volumes'
        params = {
            'q': movie_data['Title'],
            'key': GOOGLE_BOOKS_API_KEY,
        }

        response = requests.get(google_books_url, params=params)
        response.raise_for_status()

        data = response.json()

# Här får vi också ut datan som Json och väljer därefter ut vilka data vi vill ha.
        if 'items' in data:
            books = []
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', '')
                author = ', '.join(volume_info.get('authors', []))
                info_link = volume_info.get('infoLink', '')
                thumbnail = volume_info.get('imageLinks', {}).get('smallThumbnail', '')

                books.append({'title': title, 'author': author, 'link': info_link, 'thumbnail': thumbnail})

            return books
    except requests.exceptions.RequestException as e:
        print(f"Error with Google Books API request: {e}")
    
    return None

if __name__ == '__main__':
    app.run(debug=True)
