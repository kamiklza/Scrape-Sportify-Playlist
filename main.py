from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import SpotifyOAuth
from pprint import pprint



OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'
client_id = "dc553f195eed415dae3fd2eee33d1f1e"
client_secret = "00688d496c48419bbc423f836bd764d1"
redirect_url = "http://127.0.0.1:5500/"
play_list_id = "535ayeZP2jasdVA5NvexoX"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_url,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]



time_to_travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{time_to_travel}")
website = response.text

soup = BeautifulSoup(website, "html.parser")
titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")


#-------Search song title uri----------#
list_of_uri = []
for title in titles:
    song_data = sp.search(q=title.getText(), limit=1, type="track", market="US")
    try:
        song_uri = song_data["tracks"]["items"][0]["uri"]
    except IndexError:
        continue
    else:
        list_of_uri.append(song_uri.strip("'"))
print(list_of_uri)
print(len(list_of_uri))

#-----Create Playlist and get the playlist id---------#
# play_list = sp.user_playlist_create(user=user_id, name=f"{time_to_travel} Billboard 100", public=False)
# play_list_id = play_list["id"]
# print(play_list_id)

sp.playlist_add_items(playlist_id=play_list_id, items=list_of_uri)





