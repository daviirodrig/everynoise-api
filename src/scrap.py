from bs4 import BeautifulSoup
import requests


def scrap_artist_genres(artist: str):
    url = "https://everynoise.com/lookup.cgi"
    str_html = requests.get(f"{url}?who={artist}").content

    bs = BeautifulSoup(str_html, "lxml")

    links = bs.find_all("a")

    return [i.text for i in links[:-2]]


def scrap_genre_page(genre: str):
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
                "song_title": div.attrs.get("title")[5:]
                if div.attrs.get("title") != "(no sample available)"
                else "",
                "style": [i.strip() for i in div.get("style").split(";")],
            }
        )

    for element in title_div.children:
        try:
            element_href = str(element.attrs.get("href"))
            if element_href.startswith("https://open.spotify.com"):
                final["playlists"].append({element.text: element_href})
        except AttributeError:
            pass

    return final


def scrap_home_genres_page():
    """
    Scraps the home of everynoise.com

    Returns a dict with genre, preview_url, song_title and style
    """
    url = "https://everynoise.com/engenremap.html"
    req = requests.get(url)
    if req.status_code == 404:
        return {"genres": [], "playlists": []}
    str_html = req.content
    bs = BeautifulSoup(str_html, "lxml")

    divs = bs.find_all("div", class_="genre scanme")
    title_div = bs.find("div", class_="title")
    final = {"genres": [], "playlists": []}

    for div in divs:
        final["genres"].append(
            {
                "name": div.text[:-2],
                "preview_url": div.get("preview_url"),
                "song_title": div.attrs.get("title")[5:]
                if div.attrs.get("title") != "(no sample available)"
                else "",
                "style": [i.strip() for i in div.get("style").split(";")],
            }
        )

    for element in title_div.children:  # type: ignore
        try:
            element_href = str(element.attrs.get("href"))  # type: ignore
            if element_href.startswith("https://open.spotify.com"):
                final["playlists"].append({element.text: element_href})
        except AttributeError:
            pass

    return final
