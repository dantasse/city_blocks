#!/usr/bin/env python

# Take in a geojson file of neighborhood shapes, output some kind of 3D shapes
# for use in Rhino based on them.

import geojson, shapely.geometry, argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--neighborhoods_filename', default='Pittsburgh_Neighborhoods.json')
    args = parser.parse_args()
    neighborhoods = geojson.load(open(args.neighborhoods_filename))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd.geometry)
    
