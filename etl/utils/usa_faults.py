"""US Fault Lines"""

import os

import geopandas as gpd
from utils.db import upload_and_postprocess
from utils.extraction import DATA_FOLDER, download_and_extract_zipfile

URL_USA_FAULTS = "https://earthquake.usgs.gov/static/lfs/nshm/qfaults/Qfaults_GIS.zip"

if __name__ == "__main__":
    download_and_extract_zipfile(URL_USA_FAULTS, "usa_faults.zip")
    faults = gpd.read_file(os.path.join(DATA_FOLDER, "SHP", "Qfaults_US_Database.shp"))
    upload_and_postprocess(faults, "usa_faults")
