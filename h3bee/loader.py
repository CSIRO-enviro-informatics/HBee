import os 
import glob
import subprocess
import zipfile 
import psycopg2
from psycopg2 import sql

def create_data_table():
    conn = psycopg2.connect("user='postgres' host='localhost' port=5433 password='password'")
    cursor = conn.cursor()
    cursor.execute("drop table if exists data_table; create table data_table (id_c jsonb, h3_l11 h3index);")
    conn.commit()

def sample_table(table_name):
    conn = psycopg2.connect("user='postgres' host='localhost' port=5433 password='password'")
    cursor = conn.cursor()
    cursor.execute(
            "SELECT string_agg(quote_ident(attname), ', ' ORDER BY attnum) FROM pg_attribute WHERE  attrelid = %(table_name)s::regclass AND NOT attisdropped AND attnum > 0 AND attname <> 'geom_4326'", {'table_name' : 'public.'+table_name})

    # Do string interpolation carefully because can't use variable substitution directly
    columns_to_get = ["'" + sql.Identifier(ident.replace("'", "").replace('"', '').strip()).as_string(conn) + "', " + sql.Identifier(ident.replace("'", "").replace('"', '').strip()).as_string(conn) for ident in cursor.fetchone()[0].split(',')]
    print(columns_to_get)
    cursor = conn.cursor()
    cursor.execute(
            'insert into data_table select jsonb_build_object(' + ', '.join(columns_to_get) + ') as id_c, h3_to_parent(h3_polyfill(geom_4326, 14), 5) as h3_l11 from ' + table_name + ' group by id_c, h3_l11')
    print(cursor.query)
    conn.commit()
    #print(cursor.fetchall())

datasets = [ "https://data.gov.au/dataset/1f554890-454d-49e9-8d97-d787d991106c/resource/2be67b17-6164-49e2-a838-5e6b5f6d3067/download/cogb-planning-bmo.shz",
"https://data.gov.au/dataset/1a478d6e-fddd-4d00-a61a-c2d196562db0/resource/b49940db-2091-4846-899f-a3070859ae8d/download/cogb-assets-footpath.shz",
"https://data.gov.au/dataset/1ac84b6c-aef0-445f-a8da-0f19d0796181/resource/0974d3f1-6c17-47a0-9ee9-cfc608fd0012/download/wyndham-city-building-footprints.shz",
"https://data.gov.au/dataset/1d580398-bda9-432c-93b3-557a4a0b006b/resource/a096c07f-cdc0-48fa-b219-ae79e447fba5/download/cogb-assets-sealed-roads.shz",
"https://data.gov.au/dataset/1f554890-454d-49e9-8d97-d787d991106c/resource/2be67b17-6164-49e2-a838-5e6b5f6d3067/download/cogb-planning-bmo.shz",
"https://data.gov.au/dataset/275fd032-a321-4534-8fff-19fffe3e52c2/resource/63c55991-61a2-4fb5-b0c3-8f50bcc1dc8c/download/buildingfootprints_2017.shz",
"https://data.gov.au/dataset/34c4cd01-3886-4e4e-b78e-97368db7275c/resource/70892751-2586-4729-a616-bf19c8317e8d/download/wyndham-city-public-toilets.shz",
"https://data.gov.au/dataset/3df55d47-8fde-4f2d-97a6-ba51bdbad0cb/resource/8d37d3d8-c171-48b8-b65b-93ba57e3d442/download/cogb-community-mach-zones.shz",
"https://data.gov.au/dataset/3edf7196-48a9-4bf0-87ce-29b323ae5de9/resource/2687f589-341f-4c36-bbf2-1f9c754ae9dc/download/wyndham-city-libraries.shz",
"https://data.gov.au/dataset/42f5dcf2-c81f-4ceb-a831-b62523d4773e/resource/273fc321-3596-4b71-85ea-25e4f45ff024/download/wyndham-city-maternal-child-health.shz",
"https://data.gov.au/dataset/44160b34-8c87-4cd2-9212-a5cd6bd40f37/resource/3b143bd4-b5e7-4a78-b410-5d7936ee9d4c/download/floodstudyoverlays.shz",
"https://data.gov.au/dataset/20df136e-f375-4c2a-b093-db1b40833f14/resource/d96de336-3847-4db2-bc29-95f2ca5e663f/download/vectorpackageclumc0917.zip" ]

overall_count = 0

"""
try:
    for num, aUri in enumerate(datasets): 
        afile = 'data_file_{}'.format(num)
        subprocess.run(['wget', '-O', afile, aUri], check=True)
        with zipfile.ZipFile(afile, 'r') as zip_ref:
            zip_ref.extractall("data_dir_{}".format(num))
        overall_count += 1
except:
    pass
"""
shape_files_to_process = [] 
for x in range(0, len(datasets)-1): 
    shape_files = glob.glob('./data_dir_{}/*.shp'.format(x))
    shape_files_to_process.append(shape_files[0])

create_data_table()
for num, process_file in enumerate(shape_files_to_process): 
    subprocess.run(['ogr2ogr', '-f', 'PostgreSQL', 'PG:host=localhost port=5433 user=postgres password=password', './{}'.format(process_file), '-skipfailures', '-overwrite', '-progress', '-nln', 'data_table_{}'.format(num), '-nlt', 'MULTIPOLYGON', '-lco', 'GEOMETRY_NAME=geom_4326', '-lco', 'PRECISION=NO', '-t_srs', 'EPSG:4326', '--config', 'PG_USE_COPY', 'YES'], check=True)

for x in range(0, len(datasets)-1): 
    try:
        sample_table('data_table_{}'.format(x))
    except:
        continue
