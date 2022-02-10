"""Tectonic Plates

Data from a 2003 paper by Peter Bird. (Geochemistry Geophysics Geosystems, 4(3), 1027,
[doi:10.1029/2001GC000252](http://scholar.google.se/scholar?cluster=1268723667321132798), 2003).
Converted to vector by Hugo Ahlenius of Nordpil in this repo:
https://github.com/fraxen/tectonicplates
"""


import os

import geopandas as gpd
from utils.db import upload_and_postprocess
from utils.extraction import DATA_FOLDER, download_and_extract_zipfile

PLATES_URL = "https://github.com/fraxen/tectonicplates/archive/master.zip"


def read_plates(shp_file="PB2002_plates.shp"):
    """Read the tectonic plates shapefile"""
    gdf = gpd.read_file(os.path.join(DATA_FOLDER, "tectonicplates-master", shp_file))

    return gdf


if __name__ == "__main__":
    download_and_extract_zipfile(PLATES_URL, "plates.zip")
    plates_gdf = read_plates()
    plates_gdf = plates_gdf.drop(columns=["LAYER"])
    upload_and_postprocess(plates_gdf, "plates")
