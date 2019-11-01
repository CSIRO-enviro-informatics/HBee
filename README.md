# H3Bee - Fast Approximate Deep Spatial Catalog

This is a work in progress to provide deep but approximate indexing to the individual record level in spatial datasets. In traditional data catalogs spatial data and associated spatial metadata describes a bounding box around the whole dataset but no detail into the data contained per spatial boundary or record within. For large numbers of datasets fully storing, indexing and searching across detailed spatial boundaries per records isn't computationally feasible. H3 is a hierarchical spatial index that provides approximate spatial boundaries at multiple resolutions. H3 is employed with postgis to allow spatial data to be ingested processed into compact H3 representations and then compressed by throwing away detailed spatial boundaries but keeping approximations for deep approximate searches. 

# Running

`docker-compose up -d` brings up a H3 enabled postgis database.

`h3bee/loader.py` to download and load some data

pgAdmin4 (at the moment) to do queries and find stuff e.g

## To visualise the "hive" i.e hexagonal h3 boundaries of some approximately indexed data

`select *, h3_to_geo_boundary_geometry(h3_l11, false) as h3_indexes_found from data_table limit 3000`

## To deep find approximately indexed shapes across datasets at a location (and visualise the "hive")  

`select *, h3_to_geo_boundary_geometry(h3_l11, false)  from data_table where h3_l11 = h3_geo_to_h3(POINT('144.285527, -36.752529'), 5)`
