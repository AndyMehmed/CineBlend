# Importera nödvändiga moduler: Flask för webramverket, render_template för att rendera HTML-sidor, request för att hantera HTTP-request, requests för att göra HTTP-request och config för att hämta API-nycklar.
from flask import Flask, render_template, request
import requests
import config

# Skapa en Flask-appinstans.
app = Flask(__name__)

# Hämta API-nycklar från config-filen.
OMDB_API_KEY = config.OMDB_API_KEY
GOOGLE_BOOKS_API_KEY = config.GOOGLE_BOOKS_API_KEY

# Ange sökväg till mapp med HTML-templates för appen.
app.template_folder = "templates"

# Definiera huvudrouten för appen.
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initiera variabel för att lagra filmdata.
    movie_data = None

    # Kontrollera om en POST-request har skickats, vilket indikerar att användaren har skickat in en sökning.
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        # Kontrollera att användaren faktiskt har skrivit in något i sökfältet.
        if user_input:
            try:
                # Hämta filmdata från OMDb API baserat på användarens inmatning.
                movie_data = get_movie_data(user_input)

                if movie_data:
                    # Hämta bokrekommendationer baserat på filmdata.
                    book_recommendations = get_book_recommendations(movie_data)
                    return render_template('index.html', movie=movie_data, books=book_recommendations)
                else:
                    return render_template('index.html', error='The movie was not found. Please try again.')
            except requests.exceptions.RequestException as e:
                print(f"Error fetching movie data: {e}")
                return render_template('index.html', error='An error occurred while fetching movie data.')

    # Rendera index.html med filmdata.
    return render_template('index.html', movie=movie_data)


# Funktion för att hämta filmdata från OMDb API baserat på filmnamn.
def get_movie_data(movie_title):
    try:
        # Bygg upp URL för OMDb API-anrop med API-nyckel och önskat filmtitel.
        omdb_url = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}&plot=full'
        response = requests.get(omdb_url)
        response.raise_for_status()

        # Bearbeta JSON-svar och välj ut relevant filmdata som ska visas.
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

# Funktion för att hämta bokrekommendationer baserat på filmdata från Google Books API.
def get_book_recommendations(movie_data):
    try:
        # Bygg upp URL för Google Books API-anrop med API-nyckel och önskad filmtitel.
        google_books_url = 'https://www.googleapis.com/books/v1/volumes'
        params = {
            'q': movie_data['Title'],
            'key': GOOGLE_BOOKS_API_KEY,
        }

        response = requests.get(google_books_url, params=params)
        response.raise_for_status()

        # Bearbeta JSON-svar och välj ut relevant bokdata.
        data = response.json()

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

# Starta appen om skriptet körs direkt.
if __name__ == '__main__':
    app.run(debug=True)
