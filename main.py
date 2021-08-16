import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint


#please register with Spotify API to obtain your own client_id and client_secret
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/search"

date_in_the_past = input("What date in the past do you want to return back to? (YYYY/mm/dd) ")
formatted_date_in_the_past = date_in_the_past.split("/")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{formatted_date_in_the_past[0]}-"
                        f"{formatted_date_in_the_past[1]}-{formatted_date_in_the_past[2]}")

billboard_html = response.text


soup = BeautifulSoup(billboard_html, "html.parser")

top_songs = soup.findAll(name="span", class_="chart-element__information__song text--truncate color--primary")
# artists = soup.findAll(name="span", class_="chart-element__information__artist text--truncate color--secondary")

songs_list = [song.getText() for song in top_songs]
# artists_list = [artist.getText() for artist in artists]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog="True",
                                               cache_path="token.txt"))

user_id = sp.current_user()["id"]

song_uris = []

for song in songs_list:
    result = sp.search(q=f"track:{song} year:{formatted_date_in_the_past[0]}", type="track")
    # pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user="6kjlqj5ir0eyxzxw115b47xtx", name=f"{formatted_date_in_the_past[0]}-{formatted_date_in_the_past[1]}"
                                              f"-{formatted_date_in_the_past[2]} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


print(sp.playlist(playlist_id=playlist["id"]))



#SPOTIFY DOCUMENTATION
# for song in songs_list:
#     parameters = {
#         "q": song,
#         "type": "track",
#         "year": f"{formatted_date_in_the_past[0]}",
#     }
#
#     header = {
#         "access_token": "BQCY_a8L9pfMLeKWopz6QikwWcl6vh0ZCgmg8z7kxV2_2Ghq6MH7tZNV3vvK8greRBKMra1UNgxURanh9xcSBQidwy46DJpABYLtGk3BkA3--XiXnJR36N_Akk8KQjdaePjU6rHpgz6pH1wpcvZjp-B8DuvUIwvaT7n5XdiTdH34rOT3FoFXHVWJgLMbRyGyAA",
#         "token_type": "Bearer",
#         "expires_in": 3600,
#         "refresh_token": "AQANqZXN9qFIxQ1w_sEBCouxrW-eMxq2yITI36C52CqaoCMm1rSvAZ9hhvy2hWiZEGO7o99ZMX4-OYqbuuxUJfF9SknMSqz8UyAS4jM2b9yXI5XI1ncVhaepYE4zuXye9lk",
#         "scope": "playlist-modify-private",
#         "expires_at": 1625520375
#     }
#
#     response = requests.get(url=SPOTIFY_ENDPOINT, params=parameters, headers=header)
#     result = response.json()
#     print(result)