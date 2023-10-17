import json
import os
import logging
import math

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_geojson(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        return None

def extract_ways(geojson_data):
    ways_dict = {}
    for feature in geojson_data['features']:
        # Check if the feature is a way
        if feature['geometry']['type'] in ['Linestring', 'Polygon']:
            way_id = feature['id']
            ways_dict[way_id] = feature
    return ways_dict

def process_all_geojson_files(directory):
    all_ways = {}
    for filename in os.listdir(directory):
        if filename.endswith('.geojson'):
            filepath = os.path.join(directory, filename)
            geojson_data = load_geojson(filepath)
            if geojson_data:
                ways_dict = extract_ways(geojson_data)
                all_ways.update(ways_dict)
    return all_ways

# Process all GeoJSON files in the specified directory
directory_path = 'D:\Documents\OSM-Derivative-Database\geojson_sample_data'
all_ways_dict = process_all_geojson_files(directory_path)

try:
    with open('all_ways.json', 'w') as file:
        json.dump(all_ways_dict, file)
    logging.info("Saved all_ways.json successfully.")
except Exception as e:
    logging.error(f"Error saving all_ways.json: {e}")

intersections_dict = {}

def find_intersections(way_A, way_B):
    # This function will return a list of intersecting points between two ways
    intersections = []
    for point_A in way_A:
        for point_B in way_B:
            if point_A == point_B:
                intersections.append(point_A)
    return intersections

for way_id_A, way_A in all_ways_dict.items():
    for way_id_B, way_B in all_ways_dict.items():
        # Skip comparing the way with itself
        if way_id_A == way_id_B:
            continue
        
        # Find intersections between way_A and way_B
        intersecting_points = find_intersections(way_A['geometry']['coordinates'][0], way_B['geometry']['coordinates'][0])
        
        # If intersections are found, store them
        if intersecting_points:
            if way_id_A not in intersections_dict:
                intersections_dict[way_id_A] = []
            intersections_dict[way_id_A].extend(intersecting_points)

try:
    with open('intersections.json', 'w') as file:
        json.dump(intersections_dict, file)
    logging.info("Saved intersections.json successfully.")
except Exception as e:
    logging.error(f"Error saving intersections.json: {e}")



segmented_ways = []

for way_id_A, way_A in all_ways_dict.items():
    way_coordinates = way_A['geometry']['coordinates'][0]

    if way_id_A in intersections_dict:
        intersections = intersections_dict[way_id_A]
        sorted_intersections = sorted(intersections, key=lambda x: way_coordinates.index(x))

        start_index = 0
        for intersection in sorted_intersections:
            end_index = way_coordinates.index(intersection)
            segment = way_coordinates[start_index:end_index+1]
            segmented_ways.append((segment, way_id_A))  # Store segment with its original way ID
            start_index = end_index

        segment = way_coordinates[start_index:]
        if segment:
            segmented_ways.append((segment, way_id_A))  # Store segment with its original way ID
    else:
        segmented_ways.append((way_coordinates, way_id_A))  # Store segment with its original way ID

try:
    with open('segmented_ways.json', 'w') as file:
        json.dump(segmented_ways, file)
    logging.info("Saved segmented_ways.json successfully.")
except Exception as e:
    logging.error(f"Error saving segmented_ways.json: {e}")

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_segment_distance(segment):
    total_distance = 0
    for i in range(len(segment) - 1):
        point1 = segment[i]
        point2 = segment[i + 1]
        total_distance += haversine_distance(point1[1], point1[0], point2[1], point2[0])
    return total_distance

def calculate_bounding_box(segment):
    min_lat = min([point[1] for point in segment])
    max_lat = max([point[1] for point in segment])
    min_lon = min([point[0] for point in segment])
    max_lon = max([point[0] for point in segment])
    return [(min_lat, min_lon), (max_lat, max_lon)]

def create_geojson(segmented_ways, intersections, all_ways_dict):
    features = []
    intersection_id_counter = 1

    for intersection in intersections.values():
        for point in intersection:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": point
                },
                "properties": {
                    "id": f"intersection_{intersection_id_counter}",
                }
            }
            features.append(feature)
            intersection_id_counter += 1

    for segment_data in segmented_ways:
        segment, original_way_id = segment_data  # Unpack the tuple
        original_properties = all_ways_dict[original_way_id]['properties']

        private_access = 'yes' if original_properties.get('access') in ['private', 'no'] else 'no'
        bicycle_accessible = 'yes' if original_properties.get('bicycle') == 'yes' else 'no'
        start_intersection_id = f"start{original_way_id}"
        end_intersection_id = f"end{original_way_id}"

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": segment
            },
            "properties": {
                **original_properties,
                "distance_total": calculate_segment_distance(segment),
                "bounding_box": calculate_bounding_box(segment),
                "private_access": private_access,
                "bicycle_accessible": bicycle_accessible,
                "intersection_start_id": start_intersection_id,
                "intersection_end_id": end_intersection_id
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson

geojson_data = create_geojson(segmented_ways, intersections_dict, all_ways_dict)
with open('output.geojson', 'w') as file:
    json.dump(geojson_data, file)