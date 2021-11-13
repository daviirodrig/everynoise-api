from fastapi import FastAPI
from src.scrap import search_artist_genre, scrap_genre_page

app = FastAPI()


@app.get("/artist_genre")
def artist_genre_search(artist: str):
    result = search_artist_genre(artist)

    return {"artist": artist, "genres": result}


@app.get("/genre")
def genre_page(q: str):
    result = scrap_genre_page(q.replace(" ", ""))

    return result
