import sys
import spotipy

''' shows recommendations for the given artist
'''

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

sp.trace = False


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist):
    albums = []
    results = sp.recommendations(seed_artists=[artist['id']])
    for track in results['tracks']:
        print(track['name'], '-', track['artists'][0]['name'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(('Usage: {0} artist name'.format(sys.argv[0])))
    else:
        name = ' '.join(sys.argv[1:])
        artist = get_artist(name)
        if artist:
            show_recommendations_for_artist(artist)
        else:
            print("Can't find that artist", name)
