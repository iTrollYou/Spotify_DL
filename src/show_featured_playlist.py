import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

credenciales = []
f = open('credenciales.txt', 'r')
datos = f.read().split("\n")
credenciales.append(datos[0].split("'")[1])
credenciales.append(datos[1].split("'")[1])
f.close()
client_credentials_manager = SpotifyClientCredentials(credenciales[0],
                                                      credenciales[1])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

response = sp.featured_playlists()
print(response['message'])

while response:
    playlists = response['playlists']
    for i, item in enumerate(playlists['items']):
        print(playlists['offset'] + i, item['name'])

    if playlists['next']:
        response = sp.next(playlists)
    else:
        response = None
