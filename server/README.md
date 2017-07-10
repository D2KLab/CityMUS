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

## Docker

    docker build -t doremus/citymus .
    docker run -d -p 5080:5000 --restart=unless-stopped --name citymus doremus/citymus

    # remove
    docker stop citymus
    docker rm citymus
    docker rmi doremus/citymus
