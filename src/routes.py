from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.scrap import scrap_artist_genres, scrap_genre_page

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/search/artist/{name}")
def search_artist_route(name: str):
    result = scrap_artist_genres(name)

    return {"artist": name, "genres": result}


@app.get("/genre/{genre}")
def genre_page(genre: str):
    genre = remove_symbols(genre)
    result = scrap_genre_page(genre)

    return result


def remove_symbols(string):
    return "".join(c for c in string if c.isalnum())
