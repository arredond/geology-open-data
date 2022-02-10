"""Extraction

Utility functions to aid in data download and preprocessing
"""
import os
from zipfile import ZipFile

import requests

DATA_FOLDER = os.path.join(os.pardir, "data")


def download_and_extract_zipfile(url, zipfile_name):
    """Download a zipfile and extract to the main data folder"""
    with open(os.path.join(DATA_FOLDER, zipfile_name), "wb") as f:
        response = requests.get(url)
        f.write(response.content)

    ZipFile(os.path.join(DATA_FOLDER, zipfile_name)).extractall(DATA_FOLDER)
