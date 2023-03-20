#!/usr/bin/python3

import matplotlib.pyplot as pl
import numpy as np
import gpxpy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

import argparse
from PIL import Image

request = cimgt.OSM(cache='.')

def parse_gpx_file (gpx_file):
    gpx_file = open(gpx_file, 'r')
    return gpxpy.parse(gpx_file)

def find_gpx_bbox(gpx,min_lat,min_lon,max_lat,max_lon):
    lat_lon ={}
    wp={}
    
    for waypoint in gpx.waypoints:
        if DEBUG > 8: print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
        lat_lon['lat'] = waypoint.latitude 
        lat_lon['lon'] = waypoint.longitude
        wp[waypoint.name] = lat_lon 
        if min_lat == "":
            print("Min lat not set")
            min_lat = waypoint.latitude
            max_lat = waypoint.latitude

            min_lon = waypoint.longitude
            max_lon = waypoint.longitude
        else:
            if DEBUG >= 1: print("updat min/max")
            min_lat = min(min_lat,waypoint.latitude)
            max_lat = max(max_lat,waypoint.latitude)

            min_lon = min(min_lon,waypoint.longitude)
            max_lon = max(max_lon,waypoint.longitude)    

    return [min_lat,min_lon,max_lat,max_lon]

def plot_waypoints (gpx,colour):
    if DEBUG >= 1: print("\nINFO: Start Plot waypoints\n")
    flat=0
    flon=0

    for waypoint in gpx.waypoints:
        if flat==0:
            flat= waypoint.latitude
            flon= waypoint.longitude
        else:
            pl.plot([flon, waypoint.longitude], [flat, waypoint.latitude], transform=ccrs.PlateCarree(), linewidth=1, color=colour, marker= '>', markersize=3)
            flat= waypoint.latitude
            flon= waypoint.longitude
    if DEBUG >= 1: print("\nINFO: End Plot waypoints\n")

parser = argparse.ArgumentParser()
parser.add_argument('-g',  '--green')
parser.add_argument('-y',  '--yellow')
parser.add_argument('-p',  '--pink')
parser.add_argument('-i',  '--purple')
parser.add_argument('-gt', '--green_text')
parser.add_argument('-yt', '--yellow_text')
parser.add_argument('-pt', '--pink_text')
parser.add_argument('-it', '--purple_text')
parser.add_argument('-o',  '--out_file', required=True)
parser.add_argument('-z',  '--zoom',default=15)
parser.add_argument('-d',  '--debug',default=0)
args = parser.parse_args()

DEBUG = args.debug

if args.green == None and args.yellow==None and args.pink==None and args.purple==None:
    print("No gpx file supplied")
    exit(1)

   
#for track in gpx.tracks:
#    for segment in track.segments:
#        for point in segment.points:
#            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

#for route in gpx.routes:
#    print('Route:')
#    for point in route.points:
#        print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))


if args.green is not None:
    gpx_green = parse_gpx_file(args.green)
    min_lat,min_lon,max_lat,max_lon = find_gpx_bbox(gpx_green,"","","","")

if args.yellow is not None:
    gpx_yellow = parse_gpx_file(args.yellow)
    min_lat,min_lon,max_lat,max_lon = find_gpx_bbox(gpx_yellow,min_lat,min_lon,max_lat,max_lon)

if args.pink is not None:
    gpx_pink = parse_gpx_file(args.pink)
    min_lat,min_lon,max_lat,max_lon = find_gpx_bbox(gpx_pink,min_lat,min_lon,max_lat,max_lon)

if args.purple is not None:
    gpx_purple = parse_gpx_file(args.purple)
    min_lat,min_lon,max_lat,max_lon = find_gpx_bbox(gpx_pink,min_lat,min_lon,max_lat,max_lon)

if DEBUG >= 1:
    print(f'min_lon {min_lon}\t min_lat {min_lat}')         
    print(f'max_lon {max_lon}\t max_lat {max_lat}')    
    
x=max_lon - min_lon
y=max_lat - min_lat
# Bounds: (lon_min, lon_max, lat_min, lat_max):

extent = [(min_lon-0.0008), (max_lon+0.0008), (min_lat-0.0008), (max_lat+0.0008)]

A=4

if x < y:
    #Portrat
    fig=pl.figure(figsize=[33.11 * 0.5**(0.5 * A), 46.82 * 0.5**(0.5 * A)], dpi=300)
    #print(f'SIZE: {33.11 * 0.5**(0.5 * A)} , {46.82 * 0.5**(0.5 * A)}')
else:
    #Lanscape
    fig=pl.figure(figsize=[46.82 * 0.5**(0.5 * A), 33.11 * 0.5**(0.5 * A)], dpi=300)
    #print(f'SIZE: {46.82 * 0.5**(0.5 * A)} , {33.11 * 0.5**(0.5 * A)}')


#ax = pl.axes(projection=request.crs)
ax = fig.add_subplot(1,1,1,projection=request.crs)

ax.set_extent(extent)
print("Retrieve Map")
## 12	town, or city district
## 13	village, or suburb
## 14	thousand	
## 15	small road
## 16	street
## 17	block, park, addresses
## 18	some buildings, trees
## 19	local highway and crossing details
## 20	hundred	A mid-sized building
ax.add_image(request, args.zoom)    # 5 = zoom level

if args.green  is not None:plot_waypoints(gpx_green,'green')
if args.yellow is not None:plot_waypoints(gpx_yellow,'yellow')
if args.pink   is not None:plot_waypoints(gpx_pink,'pink')
if args.purple is not None:plot_waypoints(gpx_purple,'purple')


#pl.plot([min_lon, max_lon], [min_lat, max_lat], color='green', linewidth=2, marker='o', transform=ccrs.PlateCarree())
offset=0
if args.green_text  is not None:
    pl.text(min_lon,min_lat+offset,args.green_text, transform=ccrs.PlateCarree())
    offset=offset+0.001
if args.yellow_text  is not None:
    pl.text(min_lon,min_lat+0.001,args.yellow_text, transform=ccrs.PlateCarree())
    offset=offset+0.001
if args.pink_text  is not None:
    pl.text(min_lon,min_lat+0.002,args.pink_text, transform=ccrs.PlateCarree())
    offset=offset+0.001
if args.purple_text  is not None:
    pl.text(min_lon,min_lat+0.002,args.purple_text, transform=ccrs.PlateCarree())
    offset=offset+0.001
#([flon, waypoint.longitude], [flat, waypoint.latitude], transform=ccrs.PlateCarree(), linewidth=1, color=colour, marker= '>', markersize=3)


print(f'[{min_lon}, {min_lat}], [{max_lon}, {max_lat}]')

#pl.ax(figsize=(10,6))

if DEBUG >= 1: pl.show()

fig.savefig(f'{args.out_file}.png')

## convert png to jpg

im = Image.open(f'{args.out_file}.png')
im=im.convert('RGB')
im.save(f'{args.out_file}.jpg', quality=95)

print("\n\nEND\n\n")

