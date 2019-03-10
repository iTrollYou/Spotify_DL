import os
import requests
import youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from bs4 import BeautifulSoup
from sys import argv

credenciales = []
playlist_id = str(argv[1]).split('/')[4]
canciones = []


def main():
    get_credenciales()
    changeDirectory()
    sp_admin = authentication_spotify()
    get_tracks_from_playlist(sp_admin, playlist_id)
    download_tracks()


def get_credenciales():
    f = open('credenciales.txt', 'r')
    datos = f.read().split("\n")
    credenciales.append(datos[0].split("'")[1])
    credenciales.append(datos[1].split("'")[1])
    f.close()


def changeDirectory():
    tracks_path = './Files'
    if not os.path.exists(tracks_path):
        os.mkdir(tracks_path)
        os.chdir(tracks_path)
    else:
        os.chdir(tracks_path)


def authentication_spotify():
    client_credentials_manager = SpotifyClientCredentials(credenciales[0],
                                                          credenciales[1])
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def show_tracks(results):
    # Lista con nombres de las canciones
    # Formato -> "Nombre_Artista-Nombre_Cancion-official-audio"
    print("-------------------------------------CANCIONES-------------------------------------")
    for i, item in enumerate(results['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
        cadena = track['artists'][0]['name'] + '-' + track['name'] + '-official-audio'
        canciones.append(cadena)
    print("-----------------------------------------------------------------------------------")


def get_tracks_from_playlist(sp_admin, playlist_id):
    usuario = 'Spotify-DL'
    results = sp_admin.user_playlist(usuario, playlist_id, fields="tracks,next")
    tracks = results['tracks']
    show_tracks(tracks)
    while tracks['next']:
        tracks = sp_admin.next(tracks)
        show_tracks(tracks)


def download_tracks():
    for indice in range(0, len(canciones)):
        textToSearch = str(canciones[indice]).replace(" ", "_")
        url = "https://www.youtube.com/results?search_query=" + textToSearch
        response = requests.get(url)
        cuerpo_respuesta = response.content
        if response.status_code == 200:
            html = BeautifulSoup(cuerpo_respuesta, "html.parser")
            for vid in html.findAll(attrs={'class': 'yt-uix-tile-link'}):
                track_url = 'https://www.youtube.com' + vid['href']
                break

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([track_url])


if __name__ == '__main__':
    main()
