# DOREMUS 2 Spotify

To link the DOREMUS works to playable tracks, we are using both YouTube and Spotify API.
We wrote a script that should run for about 30 hours to link Spotify tracks with DOREMUS works.

## Installation

Dependencies:
* [Python 2.7.13](https://www.python.org/downloads/) (not the version 3)
* [_pip_ library](https://pip.pypa.io/en/stable/installing/)

      curl -O https://bootstrap.pypa.io/get-pip.py
      python get-pip.py

* [_spotipy_ library](https://github.com/plamere/spotipy)

      pip install spotipy


## Running

> Note: Preliminary results are already in this [zipped folder](https://drive.google.com/open?id=0B2m64YbMzInoVE9XU21sQ1E3Qnc). Unzip the folder and copy the `all_links` folder in this one.

For running the script:

    python spotify_getVideos.py Compositions_Doremus.csv

Now, just let the script run; if you have to switch off the computer, it is not a problem. In fact, when you re-launch the script, it restarts from where it stopped.

### Logs

Running the script, some messages are printed on the screen; you don't need to know the meaning but if you want:

| Log | Meaning |
|---|---|
|`Remaning: NUMBER` | Number of Doremus compositions remaining to link |
|`Time: TIME` | Time required so far (printed every 50 linked compositions) |
| `Request Error` | It is normally caused by the high number of requests, but they should be really rare. Running the script again, it should get also the link for the queries that caused errors |
| other messages | they depend on the spotipy library |
