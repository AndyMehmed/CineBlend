# CineBlend
CineBlend - Discovers new books based on a movie input

This web application allows users to search for movie details and provides book recommendations based on the searched movie.

Preqequisites:

Before you can run CineBlend, please make sure that you have the following:
1. Python 3.12 or Higher. Ensure that you have Python installed. You can download Python from this link: https://www.python.org/downloads/
2. OMDb API key: CineBlend uses the OMDb API to fetch movie data. Get your key by following this link: https://www.omdbapi.com/apikey.aspx
3. Google Books API key: The application uses Google Books API to recommend books. Get your API key here: 
https://developers.google.com/books

Step-by-Step setup:

1. Install Python 3.12 or higher
 * Download and install Python from python.org. 
 * Verify the installation by running the following command in your terminal:

 ```bash
 python --version
 ```
 * Make sure it shows Python 3.12 or higher. 

(2. Create and activate a virtual environment (Optional)

This step is optional but recommended as it keeps yours projects dependencies isolated from other Python projects.

* Create a virtual environment:
 * Navigate to your project directory in the terminal
 * Run the following command:
 ```bash
 python -m venv venv
 ```
 This creates a virtual environment named `venv`

* activate the virtual environment:
 * On windows:
 ```bash
 venv\Scripts\activate
 ```
 
 * on MacOS/Linux:
 ```bash
 source venv/bin/activate
 ```
Once activated your terminal prompt will chjange to show the virtual environment is active)



3. Install required Python Packages
 2.1 Open your terminal or command prompt and run the following commands to install Flask and requests:

 ```bash
 pip install Flask
 pip install requests
 ```


4. Configure API keys:

* Create a file named `config.py` in the project directory where Cineblend is located. `config.py` should be in the same directory as `app.py` 
* Open `config.py` in a text editor and add the following lines replacing `"your_key_here"` with your actual API keys. 

```bash
OMDB_API_KEY = "your_omdb_api_key_here"
GOOGLE_BOOKS_API_KEY = "your_google_books_api_key_here"
```

5. Running CineBlend
* In the terminal, navigate to the directory where CineBlend is located
* Run the application with the following command: 
```bash
python app.py
```
* Once the server starts it will display a message similar to this: 

```bash
 Running on http://127.0.0.1:5000/
```
* Open your web browser and go to the adress displayed in your console. 

6. Using the Application

* On the Cineblend homepage, enter the title of a movie you are interested in.
* Click "Search" to view details about the movie and recieve book recommendations based on the title. 

7. Enjoy!

* Please enjoy using our app!
 

Dependencies

CineBlend relies on the following:

* Python: The programming language for running the app.
* Flask: A lightweight web framework for Python.
* OMDb API: For retrieving movie data.
* Google Books API: For fetching book recommendations. 

Authors:

* Andy Mehmedovic
* Gustav Åkesson

