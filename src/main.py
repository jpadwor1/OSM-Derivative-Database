import requests
import os
import time

def download_osm_data():
    #Define the URL template
    URL_TEMPLATE = "http://www.overpass-api.de/api/xapi?way[highway=path|footway|steps|bridleway|cycleway][name=*][bbox={lng},{lat},{lng_end},{lat_end}]"

    #Define the tile dimension
    TILE_DIM = 2
    
    # Create a directory to store the downloaded files
    if not os.path.exists('osm_trail_data)'):
        os.makedirs('osm_trail_data')

    #Loop through the latitude and longitude ranges in 2x2 degree tiles
    for lat in range(24, 49, TILE_DIM):
        for lng in range(-125, -66, TILE_DIM): 
            #Construct the url
            url = URL_TEMPLATE.format(lng=lng, lat=lat, lng_end=lng+TILE_DIM, lat_end= lat+TILE_DIM)

           
            #Make the request
            response = requests.get(url)
                    
            #Check for a successful response
            if response.status_code == 200:
                #Save the data
                with open(f'osm_trail_data/osm_tile_{lat}_{lng}.osm', 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Failed to download data for tile {lat}, {lng}: {response.status_code}')
            
            time.sleep(1)

if __name__ == '__main__':
    download_osm_data()