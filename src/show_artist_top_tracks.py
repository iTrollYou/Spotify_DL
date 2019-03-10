# shows artist info for a URN or URL

import spotipy
import sys

from spotipy.oauth2 import SpotifyClientCredentials

if len(sys.argv) > 1:
    urn = sys.argv[1]
else:
    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

credenciales = []
f = open('credenciales.txt', 'r')
datos = f.read().split("\n")
credenciales.append(datos[0].split("'")[1])
credenciales.append(datos[1].split("'")[1])
f.close()
client_credentials_manager = SpotifyClientCredentials(credenciales[0],
                                                      credenciales[1])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
response = sp.artist_top_tracks(urn)

for track in response['tracks']:
    print(track['name'])
