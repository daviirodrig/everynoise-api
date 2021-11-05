from bs4 import BeautifulSoup
import requests


def search_artist_genre(artist):
    url = "https://everynoise.com/lookup.cgi"
    str_html = requests.get(f"{url}?who={artist}").text

    bs = BeautifulSoup(str_html, "html.parser")

    links = bs.find_all("a")

    return [i.text for i in links[:-2]]
