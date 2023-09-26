import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_LINK = "https://api.themoviedb.org/3"
POSTER_LINK = "https://image.tmdb.org/t/p/w500"

search_endpoint = "/search/movie"
get_movie_endpoint = '/movie'


def search_movies(key_word: str) -> list[dict]:
    params = {"api_key": os.environ["TMDB_AUTH_KEY"], "query": key_word}
    r = requests.get(API_LINK + search_endpoint, params=params)
    r.raise_for_status()
    return r.json()["results"]


def get_movie_details(movie_id: int) -> dict:
    params = {"api_key": os.environ["TMDB_AUTH_KEY"]}
    url = f'{API_LINK}{get_movie_endpoint}/{movie_id}'
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()
