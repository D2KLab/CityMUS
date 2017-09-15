from geopy.distance import vincenty
import numpy as np
import copy
from pprint import pprint
import spotipy_util

def get_near_pois(source, original_pois):
    """given a position and the poi, get three nearest ones"""

    def log2(x):
        return np.log(x)/np.log(2)

    def add_distance_wrapper(src):
        def add_distance(point):
            point['distance'] = vincenty(src, (float(point['latitude']), float(point['longitude']))).meters
            point['distance'] += 10
            point['distance_log'] = log2(point['distance'])
            return point
        return add_distance



    MAX_RADIUS = 2000

    MAX_RADIUS_LOG = log2(MAX_RADIUS)

    new_pois = copy.deepcopy(original_pois)

    add_distance_function = add_distance_wrapper(source)

    near_pois = map(add_distance_function, new_pois)

    near_pois = sorted(near_pois, key=lambda x: x['distance'])[:3]

    filtered_pois = [near_pois.pop(0)]
    filtered_pois += filter(lambda x: x['distance_log'] < MAX_RADIUS_LOG, near_pois)[:2]

    # weight part
    total_score = sum(1. / x['distance_log'] for x in filtered_pois)
    total_weight = 0
    for poi in filtered_pois:
        poi['weight'] = 1. / (total_score * poi['distance_log'])
        total_weight += poi['weight']
    for poi in filtered_pois:
        poi['weight'] = int(round(poi['weight'] * 10. / total_weight))
    return filtered_pois


def create_playlist_name(pois):
    """given a list of (id,weight), return an identifier"""

    ids = [str(x['id']) for x in pois]
    weights = [str(x['weight']) for x in pois]
    lists = zip(ids, weights)
    lists = sorted(lists, key=lambda _: (_[1], _[0]), reverse=True)

    groups = [':'.join(x) for x in lists]
    name = '_'.join(groups)
    return name



def select_tracks(playlist_name, pois, poi_artists):
    """given a playlist name, return list of tracks and related paths"""

    groups = playlist_name.split('_')
    print(groups)
    poi_weight_list = [group.split(':') for group in groups]
    track_path_list = set()

    for p_w in poi_weight_list:
        poi_index = int(p_w[0])
        weight = int(p_w[1])
        dbpedia_uri = pois[poi_index-1]['uri']

        artists_tracks_path = [poi_artists[dbpedia_uri][artist] for artist in poi_artists[dbpedia_uri]]
        artists_tracks = [dictionary['tracks'] for dictionary in artists_tracks_path]

        # create lists of tracks for each artist
        artists_zipped = [zip(*_) for _ in artists_tracks]
        artists_tracks = [a[0] for a in artists_zipped if len(a)]

        artists_path = [dictionary['path'] for dictionary in artists_tracks_path]

        # round robin through artists:
        n_tracks = 10
        count = 0

        for track_index in range(n_tracks):
            for artist_index in range(len(artists_tracks)):

                track = artists_tracks[artist_index][track_index]

                path = tuple(artists_path[artist_index])
                if (track, path) not in track_path_list:
                    track_path_list.add((track, path))
                    count += 1
                if count == weight:
                    break
            if count == weight:
                break

    return list(track_path_list)
