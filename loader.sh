#!/bin/bash
unzip cogb-planning-bmo.shz 
ogr2ogr -f PostgreSQL 'PG:host=localhost port=5433 user=postgres password=password' bmo_region.shp -skipfailures -overwrite -progress -nln bmo_region -nlt MULTIPOLYGON -lco GEOMETRY_NAME=geom_4326 -lco PRECISION=NO -t_srs EPSG:4326 --config PG_USE_COPY YES
