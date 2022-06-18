import re
from bs4 import BeautifulSoup

# import requests

# r = requests.get(
#     "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
# )

with open("movies.html", "r") as f:
    movies_html = f.read()

soup = BeautifulSoup(movies_html, "html.parser")

all_section_tags = soup.find_all(
    "section",
    class_=re.compile("^gallery__content-item gallery__content-item--gallery"),
)

all_film_tags = {
    t.find("h3", class_="title"): t.find("strong") for t in all_section_tags
}

all_films = {k.getText(): v.getText() if v else "" for k, v in all_film_tags.items()}
print(all_films)
