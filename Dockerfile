# Dockerfile
FROM postgres:16

# Install PostGIS
RUN apt-get update && \
    apt-get install -y postgis postgresql-16-postgis-3
