import os
import subprocess

def convert_osm_to_geojson():
    # Directory paths
    input_dir = 'osm_sample_data'
    output_dir = 'geojson_sample_data'
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all OSM files in the input directory
    for osm_file in os.listdir(input_dir):
        if osm_file.endswith('.osm'):
            # Construct the full paths for input OSM file and output GeoJSON file
            input_path = os.path.join(input_dir, osm_file)
            output_path = os.path.join(output_dir, osm_file.replace('.osm', '.geojson'))
            
            # Convert OSM to GeoJSON using the osmtogeojson command-line tool
            with open(output_path, 'w') as output_file:
                subprocess.run(['C:/Users/15629/AppData/Roaming/npm/osmtogeojson.cmd', input_path], stdout=output_file)

if __name__ == '__main__':
    convert_osm_to_geojson()