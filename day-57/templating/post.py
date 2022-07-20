from collections import namedtuple
import requests

Post = namedtuple("Post", ["id", "title", "subtitle", "body"])


def get_posts():
    API_URL = "https://api.npoint.io/b15ab33a00c36ac756b7"
    r = requests.get(API_URL)
    r.raise_for_status()
    posts = {
        p["id"]: Post(p["id"], p["title"], p["subtitle"], p["body"]) for p in r.json()
    }
    return posts
