"""FAO Digital Soil Map of the World (DSMW)

Source:
https://data.apps.fao.org/map/catalog/static/api/records/446ed430-8383-11db-b9b2-000d939bc5d8


Terms of Use:
```
THE DIGITAL SOIL MAP OF THE WORLD

FOOD AND AGRICULTURE ORGANIZATION OF THE UNITED NATIONS
Version 3.6, completed January 2003

(C) FAO/UNESCO, 1995
All rights reserved worldwide.

The user agrees to acknowledge the source of FAO data as follows:
'Source:  Land and Water Development Division, FAO, Rome' in any public or commercial document or map or paper reproducing FAO data, or describing studies or computations based on the use of such data.

FAO makes every effort to ensure accuracy of data but assumes no responsibility for errors and omissions in the data provided to users nor in the documentation accompanying it.

FAO reserves the right to make changes to the data, codes, classification, periodicity and series coverage. FAO also reserves all rights to change the format of the data provided to the user.

In case of breach by the user of any of the clauses contained herein, FAO reserves the right to seek appropriate compensation.

The designations employed and the presentation of the material in the maps do not imply the expression of any opinion whatsoever on the part of FAO concerning the legal or institutional status of any country, territory or sea area, or concerning the delimitation of frontiers.
```"""

import os

import geopandas as gpd
from utils.db import upload_and_postprocess
from utils.extraction import DATA_FOLDER, download_and_extract_zipfile

URL_FAO_WORLD_SOIL = "https://storage.googleapis.com/fao-maps-catalog-data/uuid/446ed430-8383-11db-b9b2-000d939bc5d8/resources/DSMW.zip"


if __name__ == "__main__":
    download_and_extract_zipfile(URL_FAO_WORLD_SOIL, "fao_world_soil.zip")
    dsmw = gpd.read_file(os.path.join(DATA_FOLDER, "DSMW.shp"))
    upload_and_postprocess(dsmw, "fao_world_soil")
