from fastapi import FastAPI
from src.scrap import search_artist_genre

app = FastAPI()


@app.get("/artist_genre")
def artist_genre_search(artist: str):
    result = search_artist_genre(artist)

    return {"artist": artist, "genres": result}
