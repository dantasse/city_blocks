#!/usr/bin/env python

# Take in a geojson file of neighborhood shapes, output some kind of 3D shapes
# for use in Rhino based on them.

import geojson, shapely.geometry, argparse, csv, json
from shapely.geometry.point import Point
from random import random

# given a point in lat, lon space, returns one in x, y, z space (close to 0 for
# easy visualizing or printing).
def transform(lat, lon):
    x = (lon + 80.0) * 1000
    y = (lat - 40.441667) * 1000
    z = 0
    return((x, y, z))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--neighborhoods_filename', default='Pittsburgh_Neighborhoods.json')
    parser.add_argument('--densities_filename', default='nghds_dwelling_densities.csv')
    parser.add_argument('--outfile', default='rhino_data.json')
    args = parser.parse_args()

    densities = {}
    for line in csv.DictReader(open(args.densities_filename)):
        densities[line['nghd']] = float(line['units_per_acre_residential'])

    neighborhoods = geojson.load(open(args.neighborhoods_filename))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd['geometry'])

    output = []
    for nghd in nghds:
        print nghd['properties']['HOOD']
        if nghd['properties']['HOOD'] in ['Lincoln-Lemington-Belmar', 'Troy Hill', 'Marshall-Shadeland', 'Mount Oliver Borough']:
            continue #ugh TODO these nghds has 2 parts blah, or Mt. Oliver is
            # not actually part of Pgh.
        coords = nghd['geometry']['coordinates'][0]
        points = [transform(c[1], c[0]) for c in coords]

        shape = nghd['shape']
 
        # generate the endpoints of the swiss cheese "pipes"
        pipes = []
        lonmin = min([pt[0] for pt in coords])
        lonmax = max([pt[0] for pt in coords])
        latmin = min([pt[1] for pt in coords])
        latmax = max([pt[1] for pt in coords])
        density = densities[nghd['properties']['HOOD']]
        num_pipes = int(max(round(25 - density), 0))
        for i in range(num_pipes):
            while True:
                lon1 = random() * (lonmax - lonmin) + lonmin
                lat1 = random() * (latmax - latmin) + latmin
                lon2 = random() * (lonmax - lonmin) + lonmin
                lat2 = random() * (latmax - latmin) + latmin
                pt1 = Point(lon1, lat1)
                pt2 = Point(lon2, lat2)
                if shape.contains(pt1) and shape.contains(pt2):
                    pipes.append((transform(lat1, lon1), transform(lat2, lon2)))
                    break
 
        output.append({'name': nghd['properties']['HOOD'], 'border': points, 'pipes': pipes})
    json.dump(output, open(args.outfile, 'w'), indent=2)

