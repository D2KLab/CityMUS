from geopy.distance import vincenty
import numpy as np
import copy


def get_near_pois(source, original_pois):
    def add_distance_wrapper(source):
        def add_distance(point):
            point['distance'] = vincenty(source, (float(point['lat']), float(point['long']))).meters
            if point['distance'] < 5:
                point['distance'] = 5
            point['distance_sqrt'] = np.sqrt(point['distance'])
            return point
        return add_distance

    MAX_RADIUS = 150
    MAX_RADIUS_SQRT = np.sqrt(MAX_RADIUS)

    new_pois = copy.deepcopy(original_pois)

    add_distance_function = add_distance_wrapper(source)

    near_pois = map(add_distance_function, new_pois)
    #print(near_pois)
    near_pois = sorted(near_pois, key=lambda x: x['distance'])[:3]

    filtered_pois = [near_pois.pop(0)]
    filtered_pois += filter(lambda x: x['distance_sqrt'] < MAX_RADIUS_SQRT, near_pois)[:2]

    # weight part
    total_score = sum(1. / x['distance_sqrt'] for x in filtered_pois)
    total_weight = 0
    for poi in filtered_pois:
        poi['weight'] = 1. / (total_score * poi['distance_sqrt'])
        total_weight += poi['weight']
    for poi in filtered_pois:
        poi['weight'] = int(round(poi['weight'] * 10. / total_weight))
    return filtered_pois


def create_playlist_name(pois):

    ids = [str(x['id']) for x in pois]
    weights = [str(x['weight']) for x in pois]
    lists = zip(ids, weights)
    lists = sorted(lists,key= lambda x: x[1],reverse=True)
    groups = [':'.join(x) for x in lists]
    name = '_'.join(groups)
    return name

