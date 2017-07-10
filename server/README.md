CityMusic app server
====================

## Installation

Dependencies:
* [Flask](http://flask.pocoo.org/docs/0.12/installation/) 0.11+
* Geopy
* spotipy
* numpy

      pip install -r requirements.txt

> Important, the version of flask should be >= 0.11. In case, uninstall and re-install the latest version.

## Run

    export FLASK_APP=main.py
    python -m flask run

## Change the user for spotify

* change the `username` in `spotipy_util.py`
* Login on [Spotify Dev Page](https://developer.spotify.com/my-applications),
  * set `citymus` as application
  * add `http://localhost` as redirect
  * copy `client_id` and `client_secret` in `spotipy_util.py`
* run the server, an authorization page ask you to accept the connection to `citymus`
  * then, copy and paste the uri

## Docker

    docker build -t doremus/citymus .
    docker run -d -p 5080:5000 --restart=unless-stopped --name citymus doremus/citymus

    # remove
    docker stop citymus
    docker rm citymus
    docker rmi doremus/citymus
