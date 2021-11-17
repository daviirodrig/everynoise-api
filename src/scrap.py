from bs4 import BeautifulSoup
from bs4.element import NavigableString
import requests


def search_artist_genre(artist):
    url = "https://everynoise.com/lookup.cgi"
    str_html = requests.get(f"{url}?who={artist}").content

    bs = BeautifulSoup(str_html, "lxml")

    links = bs.find_all("a")

    return [i.text for i in links[:-2]]


def scrap_genre_page(genre):
    url = f"https://everynoise.com/engenremap-{genre}.html"
    req = requests.get(url)
    if req.status_code == 404:
        return {"artists": [], "playlists": []}
    str_html = req.content
    bs = BeautifulSoup(str_html, "lxml")

    divs = bs.find_all("div", class_="genre scanme")
    title_div = bs.find("div", class_="title")
    final = {"artists": [], "playlists": []}

    for div in divs:
        final["artists"].append(
            {
                "name": div.text[:-2],
                "preview_url": div.get("preview_url"),
                "style": [i.strip() for i in div.get("style").split(";")],
            }
        )

    for i in title_div.children:
        if type(i) != NavigableString:
            final["playlists"].append({i.text: i.attrs.get("href")})

    return final
