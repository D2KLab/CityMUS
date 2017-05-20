import pprint
import sys
import os
import subprocess
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

clientid = '2b4bba8dba4d406a8086f33b644ddcd0'
clientsecret = 'dc13827b3900467383a12e803b10e52f'
redirect = 'http://localhost'
username = 'fabio_ellena'

#necessary to create/add track to public spotify
scope = 'playlist-modify-public'

def get_playlists_dict(username):
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists(username)
    playlist_dict = {}
    
    for playlist in playlists['items']:
        playlist_dict[playlist['name']] = playlist['id']
    return playlist_dict


def create_playlist_if_not_exist(username, playlist_name, sp,playlist_dict):
    if playlist_name not in playlist_dict:
        playlist = sp.user_playlist_create(username, playlist_name)
        playlist_dict[playlist['name']] = playlist['id']
        return True
    else:
        return False

playlist_dict = get_playlists_dict(username)
pprint.pprint(playlist_dict)            

#get token if cached, otherwise refresh, or generate new prompting to user
token = util.prompt_for_user_token(username,scope,client_id=clientid,client_secret=clientsecret,redirect_uri=redirect)
sp = spotipy.Spotify(auth=token)
sp.trace = False

#playlist name
playlist_name = 'test'

#list of spotify track ids
track_ids = ["1pAyyxlkPuGnENdj4g7Y4f", "7D2xaUXQ4DGY5JJAdM5mGP"]

if create_playlist_if_not_exist(username,playlist_name,sp,playlist_dict):
    print('playlist created')
    results = sp.user_playlist_add_tracks(username, playlist_dict[playlist_name], track_ids)
    print('tracks added')
print('end')