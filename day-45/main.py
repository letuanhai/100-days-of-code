# from collections import namedtuple

from bs4 import BeautifulSoup
import requests

# Article = namedtuple("Article", ['text', 'link', 'point'])

r = requests.get("https://news.ycombinator.com/")
r.raise_for_status()


soup = BeautifulSoup(r.text, features="html.parser")
article_tags = soup.find_all("a", class_="titlelink")
article_texts = [article_tag.text for article_tag in article_tags]
article_links = [article_tag.get("href") for article_tag in article_tags]

article_points = [
    int(tag.getText().split(" ")[0]) for tag in soup.find_all("span", class_="score")
]

max_point_index = max(range(len(article_points)), key=article_points.__getitem__)
print(
    f"""Article with max point:
Title: {article_texts[max_point_index]},
Link: {article_links[max_point_index]},
Point: {article_points[max_point_index]}"""
)
