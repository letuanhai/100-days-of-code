from collections import namedtuple
import re
from typing import Optional
import time

import requests
from bs4 import BeautifulSoup
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv.load_dotenv()

ChartItem = namedtuple("ChartItem", ["rank", "title", "artist"])

to_date = ""
while not re.fullmatch(r"[1-2]\d{3}-(0\d|1[0-2])-([0-2]\d|3[0-1])", to_date):
    to_date = input(
        "Which date do you want to travel to? Type the date in YYYY-MM-DD format: "
    )


BASE_URL = "https://www.billboard.com/charts/hot-100/"

r = requests.get(f"{BASE_URL}{to_date}/")
r.raise_for_status()

# with open("top100.html", "r") as f:
#     # f.write(r.text)
#     top100_html = f.read()

soup = BeautifulSoup(r.text, "html.parser")
result_divs = soup.find_all("div", class_="o-chart-results-list-row-container")

top100 = []
for item in result_divs:
    rank = (
        item.select_one("span.c-label.a-font-primary-bold-l")
        .getText()
        .replace("\n", "")
        .replace("\t", "")
    )
    title = (
        item.find("h3", class_="c-title").getText().replace("\n", "").replace("\t", "")
    )
    artist = (
        item.select_one("span.c-label.a-no-trucate")
        .getText()
        .replace("\n", "")
        .replace("\t", "")
    )

    new_item = ChartItem(rank, title, artist)
    top100.append(new_item)


def split_artists(chart_item: ChartItem):
    return [
        s.strip()
        for s in re.split(
            pattern=r"ft\.|featuring|featured|feat\.",
            string=chart_item.artist,
            flags=re.I,
        )
    ]


scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, redirect_uri="http://example.com")
)

sp_user_id = sp.current_user()["id"]


def find_song_on_spotify(song: ChartItem) -> Optional[str]:
    """Query for song on Spotify. Return URI of first track found or None if no match found."""
    spotify_results = sp.search(
        q=f"track: {song.title} artist:{split_artists(song)[0]}",
        type="track",
        limit=1,
    )
    try:
        return spotify_results["tracks"]["items"][0]["uri"]
    except IndexError:
        return None


def find_all_songs_on_spotify(song_list: list[ChartItem]) -> list[str]:
    spotify_song_ids = []
    for song in song_list:
        spotify_id = find_song_on_spotify(song)
        if spotify_id:
            spotify_song_ids.append(spotify_id)
        time.sleep(0.5)

    return spotify_song_ids


sp_playlist = sp.user_playlist_create(
    user=sp_user_id, name=f"{to_date} Billboard 100", public=False
)
sp_playlist_id = sp_playlist["id"]

r = sp.playlist_add_items(
    playlist_id=sp_playlist_id, items=find_all_songs_on_spotify(top100)
)
print(r)
