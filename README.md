# OSM Derivative Database

This project aims to create a derivative database from OpenStreetMap (OSM) data. The primary focus is on extracting and processing way data, specifically paths, tracks, footways, steps, bridleways, and cycleways.

## Table of Contents

- [Features]()
- [OSM Data Collection]()
- [Data Processing]()
- [Usage]()
- [Dependencies]()
- [License]()

## Features

- Download OSM way data in 2x2 degree tiles between -58 and +72 latitude.
- Extract way data from the raw OSM data.
- Identify intersections and segment the ways at these intersections.
- Calculate various attributes for each segment, such as distance and bounding box.
- Output the processed data in GeoJSON format.

## OSM Data Collection

### Step 1: Download OSM Way Data

Before processing the data, we need to fetch the raw OSM data. This project provides a script to download OSM way data in 2x2 degree tiles, specifically between -58 and +72 latitude.

> **Note**: The Overpass API has rate limits. If you're fetching a large amount of data, consider introducing delays or handling rate limit errors gracefully.

## Data Processing

After fetching the raw OSM data, the next step is to process it. This involves extracting relevant way data, identifying intersections, segmenting the ways, and calculating various attributes.

The provided script in the repository handles all these tasks and outputs the processed data in GeoJSON format.

## Usage

1. Clone the repository.
2. Run the data collection script to fetch raw OSM data.
3. Run the data processing script to process the fetched data.
4. Check the output directory for the processed GeoJSON files.

## Dependencies

- Python 3.x
- `requests` library

To install the dependencies, run:

