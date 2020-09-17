import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import os

client_id = "67e1602e48364ea7a8873d548d12a3e6"
client_secret = "9cba2321f21940c08dca2b05b33644c0"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

# 1JCe9MAwb1aE01UoAwCnOM
def spot_album_tracks(link):
    album_id = os.path.basename(link)
    results = spotify.album_tracks(album_id)
    tracklist = results['items']
    while results['next']:
        results = spotify.next(results)
        tracklist.extend(results['items'])

    with open("track.txt", "w", encoding='utf-8') as writefile:
        for track in tracklist:
            writefile.write(track['name'].rstrip())
            writefile.write('\n')
