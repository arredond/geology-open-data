# Geology Open Data

## Introduction

This is a small collection of publicly available, mostly worldwide datasets of
geological interest:

- [FAO/UNESCO Soil Map of the World](https://www.fao.org/soils-portal/data-hub/soil-maps-and-databases/faounesco-soil-map-of-the-world/en/)

- Seismicity. Three individual datasets related to seismic risk:

  - All earthquakes over magnitude 6 from 1900 (US Geological Survey)
  - Tectonic plates from a 2003 paper by Peter Bird and converted to vector
    by [Hugo Ahlenius of Nordpil](https://github.com/fraxen/tectonicplates).
  - [Fault lines (US Geological Survey)](https://www.usgs.gov/programs/earthquake-hazards/faults) - US only.
    Note: many contributors, citation is complicated.

- [Holocene Volcanoes (Smithsonian)](https://volcano.si.edu/): All 1346 volcanoes
  known to be active during the Holocene period (approximately last 10000 years).
  **Only non-commercial use**.

- [Undiscovered Oil and Gas Resources](https://pubs.er.usgs.gov/publication/ds69FF): U.S. Geological Survey (2012)

## Structure

This repository contains a series of Python scripts in the `etl` folder used to
extract all the aforementioned datasets, as well as a simple, standalone Leaflet
app (`index.html`) to visualize said data.

This app retrieves each layer as a simple GeoJSON from a free-tier Supabase
instance with Postgres 14.1 and Postgis 3.1. Some auxiliary DDL can be found in
the `sql` folder. All API calls use the public API key with only SELECT permissions.

## Usage

To execute the ETL scripts, access to the database is needed. This is configured with a
`.env` file which can be created based on the `.env.sample` file. The scripts must
be executed from the `etl/` folder. Also, an empty `data` file is required.
For example:

```bash
mkdir data
cd etl
python3 volcanoes.py
```

## Map

A simple Leaflet app shows a nice visual of the distribution of volcanoes and
seismic events along the world's tectonic plates.

## Citations / Acknowledgments

- Global Volcanism Program, 2013. Volcanoes of the World, v. 4.10.5 (27 Jan 2022). Venzke, E (ed.). Smithsonian Institution. Downloaded 10 Feb 2022. https://doi.org/10.5479/si.GVP.VOTW4-2013

- U.S. Geological Survey World Conventional Resources Assessment Team, 2013, Supporting data for the U.S. Geological Survey 2012 world assessment of undiscovered oil and gas resources: U.S. Geological Survey Digital Data Series DDS–69–FF, various pages, https://doi.org/10.3133/ds69FF.

- UNESCO. (1974). Fao-Unesco Soil Map of the world.

- Hugo Ahlenius, Nordpil and Peter Bird for their work on the world tectonic plates dataset.


## Further improvements

### Data sources

Worldwide, publicly available geological datasets with permissible licenses
are surprisingly hard to come by. Most data seems to be distributed at the
country level so looking for US specific datasets could reveal new interesting
data sources.

### Visualization

Seismic events could be animated using a Leaflet extension such as
[Leaflet.timeline](https://github.com/skeate/Leaflet.timeline).

### Performance

The Leaflet app relies on bringing in the whole datasets as a GeoJSON served
from the database, which limits us to relatively small and/or simple datasets.
To display larger amounts of dataset, a tiling strategy should be implemented,
such as serving Mapbox Vector Tiles from the database and displaying only
the relevant amount of data at a relevant resolution each time. Furthermore,
these tile requests could be cached.

Another nice idea would be to test [glify](https://robertleeplummerjr.github.io/Leaflet.glify/),
a Leaflet extension to render the map features using WebGL.
