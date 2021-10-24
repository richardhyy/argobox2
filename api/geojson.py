import datetime
import json


FEATURE_TEMPLATE = {
    "type": "Feature",
    "id": "undefined",
    "geometry": {
        "type": "undefined",
        "coordinates": []
    },
    "geometry_name": "the_geom",
    "properties": {
    }
}

FEATURE_COLLECTION_TEMPLATE = {
    "type": "FeatureCollection",
    "features": [],
    "totalFeatures": 0,
    "numberMatched": 0,
    "numberReturned": 0,
    "timeStamp": "YYYY-MM-DDTHH:MM:SS.SSSZ",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG::4326"
        }
    }
}


def create_point_feature(feature_id, coordinates, properties):
    feature = FEATURE_TEMPLATE
    feature['id'] = feature_id
    feature['geometry']['type'] = 'Point' if len(coordinates) == 1 else 'MultiPoint'
    feature['geometry']['coordinates'].append(coordinates)
    feature['properties'] = properties

    return feature


def create_point_collection(features, total_features=0):
    collectionSize = len(features)

    collection = FEATURE_COLLECTION_TEMPLATE
    collection['features'] = features
    collection['totalFeatures'] = collectionSize if total_features == 0 else total_features
    collection['numberMatched'] = collectionSize
    collection['numberReturned'] = collectionSize
    collection['timestamp'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return json.dumps(collection)
