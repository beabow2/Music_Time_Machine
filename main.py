import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100/"
Client_ID = YOUR CLIENT ID
Client_Secret = YOUR CLIENT SECRET

# ----- Scraping Billboard 100 ----- #

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(URL+date)
soup = BeautifulSoup(response.text, "html.parser")
all_songs = soup.find_all(name="h3", class_="a-no-trucate")
song_titles = [songs.getText().strip() for songs in all_songs]

# ----- Spotify Authentication ----- #

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                              redirect_uri="http://example.com",
                              client_id=Client_ID,
                              client_secret=Client_Secret,
                              show_dialog=True,
                              cache_path="token.txt"
                              )
)

user_id = sp.current_user()["id"]

year = date.split("-")[0]

# ----- Searching Spotify for songs by title and add into a playlist----- #

song_uris = []
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist["id"])

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
