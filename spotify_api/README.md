# Get Spotify Songs
To link the doremus id works with real songs, we are trying to use both Youtube and Spotify API.
We wrote a script that should run for about 30 hours to link Soptify tracks with Doremus works.

## Before all, it's necessary to install Python 2.7.13 (not the version 3) and the library spotipy go here 
### 1) To download Python  2.7.13 go here: https://www.python.org/downloads/
### 2) To install the library you can:
a) Install pip typing on the command line:
```
python get-pip.py
```
b) Add the library spotipy typing:
```
pip install spotipy
```

## The instruction to run the script are reported here:
### 1) Download the zip file "spotify_api.zip" at this link:
https://drive.google.com/open?id=0B2m64YbMzInoLWVlU2pOX1owbVk
### 2) Unzip the folder
### 3) Using the terminal, go inside the unzipped directory and launch the scipt typing:

```
python spotify_getVideos.py Compositions_Doremus.csv
```
Now, just let the script run; if you have to switch off the computer, it is not a problem. In fact, when you relaunch the script, it restarts from where it stopped.

Running the script, some messages are printed on the screen; you don't need to know the meaning but if you want:
a) "Remaning: NUMBER" -> it indicates the number of Doremus compositions that are not yet linked
b) "Time: TIME" -> it is only an indication of the time; this message is printed every 50 linked compositions; looking at the difference between two time messages you can understand how much the program is fast
c) "Request Error" -> it could happen that there are some errors, but it is not a problem because they are caused by the high number of requests.They are really rare. At the end of all the script, running it another time, we should get also the link for the query that caused the error
d) other messages could appear; they depend on the spotipy library

That's all!
