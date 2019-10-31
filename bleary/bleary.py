import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect("user='postgres' host='localhost' port=5433 password='password'")
    cursor = conn.cursor()
    cursor.execute(
        "drop table if exists temp_data; create table temp_data as select ogc_fid, h3_to_parent(h3_polyfill(geom_4326, 11), 5) as h3_l11 from bmo_region group by ogc_fid, h3_l11"
    )
    cursor = conn.cursor()
    cursor.execute("drop table bmo_region")
    conn.commit()
