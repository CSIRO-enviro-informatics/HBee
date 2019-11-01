# H3Bee - Fast Approximate Deep Spatial Catalog

This is a work in progress to provide deep but approximate indexing to the individual record level in spatial datasets. In traditional data catalogs spatial data and associated spatial metadata describes a bounding box around the whole dataset but no detail into the data contained per spatial boundary or record within. For large numbers of datasets fully storing, indexing and searching across detailed spatial boundaries per records isn't computationally feasible. H3 is a hierarchical spatial index that provides approximate spatial boundaries at multiple resolutions. H3 is employed with postgis to allow spatial data to be ingested processed into compact H3 representations and then compressed by throwing away detailed spatial boundaries but keeping approximations for deep approximate searches. 

# Running

`docker-compose up -d` brings up a H3 enabled postgis database.

`loader.sh` to load  
