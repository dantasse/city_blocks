Pittsburgh_Neighborhoods contains info about Pittsburgh neighborhoods.
neighborhoods. Original shapefiles from http://pittsburghpa.gov/dcp/gis/gis-data

geojson files created using ogr2ogr, as in this d3 demo: http://bost.ocks.org/mike/map/
example command:
ogr2ogr -f GeoJSON -t_srs EPSG:4326 neighborhoods.json Pittsburgh_Neighborhoods/Neighborhood.shp
(the -t_srs EPSG:4326 is magic to me, it changes things from whatever gridded
coordinate mumbo jumbo into regular old lat/lon - I think it’s the same as -t_srs crs:84)

nghds_dwelling_densities.csv computed by get_dwelling_densities.py in this repo:
https://github.com/dantasse/nghd_info

