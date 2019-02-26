import os
import requests
import youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from bs4 import BeautifulSoup
from sys import argv


class SpotifyDl:

    def get_credenciales(self):
        f = open('credenciales.txt', 'r')
        datos = f.read().split("\n")
        self.credenciales.append(datos[0].split("'")[1])
        self.credenciales.append(datos[1].split("'")[1])
        f.close()

    def changeDirectory(self):
        tracks_path = '../Files'
        if not os.path.exists(tracks_path):
            os.mkdir(tracks_path)
            os.chdir(tracks_path)
        else:
            os.chdir(tracks_path)

    def authentication_spotify(self):
        client_credentials_manager = SpotifyClientCredentials(self.credenciales[0],
                                                              self.credenciales[1])
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def show_tracks(self, results):
        # Lista con nombres de las canciones
        # Formato -> "Nombre_Artista-Nombre_Canción-official-audio"
        print("-------------------------------------CANCIONES-------------------------------------")
        for i, item in enumerate(results['items']):
            track = item['track']
            print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
            cadena = track['artists'][0]['name'] + '-' + track['name'] + '-official-audio'
            self.canciones.append(cadena)
        print("-----------------------------------------------------------------------------------")

    def get_tracks_from_playlist(self, sp_admin, playlist_id):
        usuario = 'Spotify-DL'
        results = sp_admin.user_playlist(usuario, playlist_id, fields="tracks,next")
        tracks = results['tracks']
        self.show_tracks(tracks)
        while tracks['next']:
            tracks = sp_admin.next(tracks)
            self.show_tracks(tracks)

    def download_tracks(self):
        for indice in range(0, len(self.canciones)):
            textToSearch = str(self.canciones[indice]).replace(" ", "_")
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

    def __init__(self):
        self.credenciales = []
        self.playlist_id = str(argv[1]).split('/')[4]
        self.canciones = []


# main bloke
spDL = SpotifyDl()
spDL.get_credenciales()
spDL.changeDirectory()
sp_admin = spDL.authentication_spotify()
spDL.get_tracks_from_playlist(sp_admin, spDL.playlist_id)
spDL.download_tracks()
