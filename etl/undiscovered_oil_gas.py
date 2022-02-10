"""U.S. Geological Survey 2012 World Assessment of Undiscovered Oil and Gas Resources

[Supporting Data](https://pubs.er.usgs.gov/publication/ds69FF).
Geodata available for download as an ESRI GeoDataBase file.

Additional data includes fractiles of probability of occurrence of undiscovered oil and gas
in these fields. We'll join this to the GeoDataFrame before uploading to the database.
"""
import os

import fiona
import geopandas as gpd
import pandas as pd
from utils.db import upload_and_postprocess
from utils.extraction import DATA_FOLDER, download_and_extract_zipfile

URL_OILGAS_GIS = "https://pubs.usgs.gov/dds/dds-069/dds-069-ff/GIS.zip"
URL_OILGAS_EXCEL = "https://pubs.usgs.gov/dds/dds-069/dds-069-ff/exceltables.zip"

if __name__ == "__main__":
    download_and_extract_zipfile(URL_OILGAS_GIS, "oilgas_gis.zip")
    download_and_extract_zipfile(URL_OILGAS_EXCEL, "oilgas_excel.zip")

    # Read geodata and lookup data
    gdb_path = os.path.join(DATA_FOLDER, "GIS", "DDS69ff.gdb")
    fractiles_path = os.path.join(DATA_FOLDER, "Excel tables", "AU Fractiles.xlsx")
    print("Available layers in GDB:", fiona.listlayers(gdb_path))  # To inspect GDB
    wep_au = gpd.read_file(gdb_path, layer="WEP_AU")
    au_fractiles = pd.read_excel(fractiles_path)

    # Join fractiles to geodata
    au_fractiles["AU Code"] = au_fractiles["AU Code"].astype(str)
    au_fractiles = au_fractiles.rename(
        columns={
            "AU Code": "au_code",
            "Overall Oil Field Probability": "overall_oil_prob",
            "Overall Gas Field Probability": "overall_gas_prob",
        }
    )

    au_fractiles = au_fractiles.set_index("au_code")[
        ["overall_oil_prob", "overall_gas_prob"]
    ]
    wep_au = wep_au.set_index("AU_CODE").join(au_fractiles).reset_index()

    # Format and upload to database
    upload_and_postprocess(wep_au, "undiscovered_oil_gas")
