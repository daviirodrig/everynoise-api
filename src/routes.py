from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.scrap import search_artist_genre, scrap_genre_page

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/artist")
def artist_genre_search(q: str):
    result = search_artist_genre(q)

    return {"artist": q, "genres": result}


@app.get("/genre")
def genre_page(q: str):
    result = scrap_genre_page(q.replace(" ", ""))

    return result
