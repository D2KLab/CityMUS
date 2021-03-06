from pprint import pprint
import spotipy
import spotipy.util
import util
from spotipy.oauth2 import SpotifyClientCredentials


clientid = '4b115cf521ba4691a64a622eb3158f44'
clientsecret = '8d8e24a769cf4f6797e6325b33b16016'
redirect = 'http://localhost'
username = 'doremus_fr'

# necessary to create/add track to public spotify
scope = 'playlist-modify-public'

# get token if cached, otherwise refresh, or generate new prompting to user
token = spotipy.util.prompt_for_user_token(username,scope,client_id=clientid,client_secret=clientsecret,redirect_uri=redirect)
sp = spotipy.Spotify(auth=token)
sp.trace = False


def get_playlists_dict(pois,poi_artists):
    global sp
    client_credentials_manager = SpotifyClientCredentials(client_id=clientid,client_secret=clientsecret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists(username)
    playlist_dict = dict()

    for playlist in playlists['items']:
        name = playlist['name']
        tracks_paths = util.select_tracks(name,pois,poi_artists)
        playlist_object = dict()
        playlist_object['name'] = name
        playlist_object['id'] = playlist['id']
        playlist_object['tracks_paths'] = tracks_paths
        playlist_dict[playlist['name']] = playlist_object
    return playlist_dict


def create_playlist(playlist_name):
    global token
    global sp

    try:
        playlist = sp.user_playlist_create(username, playlist_name)
    except spotipy.SpotifyException:
        token = spotipy.util.prompt_for_user_token(username, scope, client_id=clientid, client_secret=clientsecret,
                                                   redirect_uri=redirect)
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlist = sp.user_playlist_create(username, playlist_name)
    return playlist


def add_tracks(playlist_id,track_ids):
    global token
    global sp

    try:
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    except spotipy.SpotifyException:
        token = spotipy.util.prompt_for_user_token(username, scope, client_id=clientid, client_secret=clientsecret,
                                                   redirect_uri=redirect)
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)


def get_artist_tracks(artist_name):
    sp = spotipy.Spotify()
    sp.trace = False

    # get matching artist

    results = sp.search(q='artist:' + artist_name, type='artist')
    artists = results['artists']['items']
    artist = None
    if len(artists) == 0:
        return None
    artist = max(artists, key=lambda x: x['popularity'])

    top_tracks = sp.artist_top_tracks(artist['id'], country='FR')['tracks']
    return_tracks = []
    for track in top_tracks:
        return_tracks.append((track['id'], track['name']))
    return return_tracks
