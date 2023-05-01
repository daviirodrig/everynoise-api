import json
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.scrap import scrap_artist_genres, scrap_genre_page, scrap_home_genres_page
import os

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


@app.get("/genres")
async def genres_page():
    # check if file exists
    if not os.path.isfile("genres_cached.json"):
        print(" [GENRES]no cache file, requesting")
        result = scrap_home_genres_page()
        with open("genres_cached.json", "w") as f:
            data = {}
            data["timestamp"] = round(time.time())
            data["data"] = result
            json.dump(data, f, indent=4)
        return result

    with open("genres_cached.json", "r+") as f:
        data = json.loads(f.read())
        if data["timestamp"] > round(time.time() - (60 * 60 * 24 * 7)):
            print("[GENRES] cache file is valid")
            return data["data"]
        else:
            print("[GENRES] Cache expired, requesting")
            result = scrap_home_genres_page()
            f.flush()
            f.seek(0)
            data = {}
            data["timestamp"] = round(time.time())
            data["data"] = result
            json.dump(data, f, indent=4)
        return result


def remove_symbols(string):
    return "".join(c for c in string if c.isalnum())
