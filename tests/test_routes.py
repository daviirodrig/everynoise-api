from src.routes import artist_genre_search


def test_artist_genre_search():
    result = artist_genre_search("do not exist7")
    assert result == {"artist": "do not exist7", "genres": []}
