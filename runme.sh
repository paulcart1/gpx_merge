#!/bin/bash

source ./env/bin/activate
echo -e "\nZOOM 15\n"
./gpx_merge.py \
    -o test_15 \
    -p route1.gpx  \
    -g route2.gpx \
    -i route3.gpx \
    -z 15 

echo -e "\nZOOM 16\n"
./gpx_merge.py \
    -o test_16 \
    -p route1.gpx  \
    -g route2.gpx \
    -i route3.gpx \
    -z 16 

echo -e "\nZOOM 17\n"
./gpx_merge.py \
    -o test_17 \
    -p route1.gpx  \
    -g route2.gpx \
    -i route3.gpx \
    -z 17 

echo -e "\nZOOM 18\n"
./gpx_merge.py \
    -o test_18 \
    -p route1.gpx  \
    -g route2.gpx \
    -i route3.gpx \
    -z 18 

echo -e "\nOSM Cache Size:\n\n\t `du -khs OSM`\n\n"

eom test_15.jpg test_16.jpg test_17.jpg test_18.jpg


