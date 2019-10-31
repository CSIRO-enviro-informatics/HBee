FROM mdillon/postgis:11
RUN apt-get update
RUN apt-get install -y python3-pip postgresql-server-dev-11 git cmake
RUN pip3 install Pyrseas
RUN pip3 install pgxnclient
RUN pgxn install h3
RUN mv /docker-entrypoint-initdb.d/postgis.sh /docker-entrypoint-initdb.d/00_postgis.sh
ADD 99_load_pgxn.sh /docker-entrypoint-initdb.d/ 

#RUN pgxn load h3