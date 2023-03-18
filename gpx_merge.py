#!/usr/bin/python3

import matplotlib.pyplot as pl
import numpy as np
import gpxpy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

DEBUG = 0

request = cimgt.OSM()

gpx_file = open('Silver2023PracticeGreenDay1.gpx', 'r')

gpx = gpxpy.parse(gpx_file)


lat_lon ={}
wp={}
#for track in gpx.tracks:
#    for segment in track.segments:
#        for point in segment.points:
#            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

#<bounds minlat="50.9584770" minlon="-1.0271670" maxlat="50.9936480" maxlon="-0.9560900"/>

min_lat = ""
min_lon = ""
max_lon = ""
max_lon = ""
#0.0
for waypoint in gpx.waypoints:
    if DEBUG > 8: print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
    lat_lon['lat'] = waypoint.latitude 
    lat_lon['lon'] = waypoint.longitude
    wp[waypoint.name] = lat_lon 
    if min_lat == "":
        min_lat = waypoint.latitude
        max_lat = waypoint.latitude

        min_lon = waypoint.longitude
        max_lon = waypoint.longitude
    else:
        min_lat = min(min_lat,waypoint.latitude)
        max_lat = max(max_lat,waypoint.latitude)

        min_lon = min(min_lon,waypoint.longitude)
        max_lon = max(max_lon,waypoint.longitude)
    


print(f'min_lon {min_lon:2.4}\t min_lat {min_lat:2.4}')         
print(f'max_lon {max_lon:2.4}\t max_lat {max_lat:2.4}')    
    

#for route in gpx.routes:
#    print('Route:')
#    for point in route.points:
#        print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))


# Bounds: (lon_min, lon_max, lat_min, lat_max):
extent = [(min_lon-0.0008), (max_lon+0.0008), (min_lat-0.0008), (max_lat+0.0008)]

x= max_lon -min_lon
y= max_lat -min_lat
area = x*y


print(f'x={x} y={y} area={area}')



#extent = [-0.9806340,-1.9806340 , 50.9638920,51.9638920]


ax = pl.axes(projection=request.crs)
ax.set_extent(extent)
ax.add_image(request, 18)    # 5 = zoom level


flat=0
flon=0
for waypoint in gpx.waypoints:
    if flat==0:
        flat= waypoint.latitude
        flon= waypoint.longitude
    else:
        #print(f'{flon} {flat} {waypoint.longitude} {waypoint.latitude}')
        pl.plot([flon, waypoint.longitude], [flat, waypoint.latitude], transform=ccrs.PlateCarree(), linewidth=1, color='green', marker= 'o', markersize=1)
        flat= waypoint.latitude
        flon= waypoint.longitude
    #pl.scatter(waypoint.longitude, waypoint.latitude, transform=ccrs.PlateCarree(),c='blue')

#pl.plot([min_lon, max_lon], [min_lat, max_lat], color='green', linewidth=2, marker='o', transform=ccrs.PlateCarree())



print(f'[{min_lon}, {min_lat}], [{max_lon}, {max_lat}]')

#pl.ax(figsize=(10,6))

#pl.show()
pl.savefig('map.png')


print("\n\nEND\n\n")
