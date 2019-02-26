# Spotify_Dl
Aplicación que descarga canciones dada una playlist de Spotify
## Precondiciones
- Cuenta en Spotify
- Python 3.x
- pip
- virtualenv

		pip install virtualenv


## Instrucciones
- Identificarse en Spotify Developers:

		https://developer.spotify.com/dashboard/applications

- Crear un Client ID y modificar el archivo "credenciales" con vuestras claves. Ejemplo:

        client_id='<Clave pública>'
        client_secret='<Clave privada>'

- Ejecutar virtualEnv:
	
		sh virtualEnv.sh
		
- Activar el entorno virtual:
	
		source venv/bin/activate

- Ejectuar la aplicación  pasando como argumento la URL de la playlist que se desea descargar:
	
		python spotify_dl.py <URL_PLAYLIST_SPOTIFY>

Enjoy :)


