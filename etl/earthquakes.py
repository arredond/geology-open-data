"""Earthquakes

A complete list for direct download is, sadly, not available. We can directly
perform queries and retrieve results as CSV but there's a limitation of 20k rows.
"""

from io import StringIO

import pandas as pd
import requests
from utils.db import upload_and_postprocess


def get_earthquakes(min_magnitude=6):
    """Return all earthquakes above a minimum magnitude as a Pandas DataFrame"""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query.csv?"

    params = {
        "starttime": "1900-01-01 00:00:00",
        "endtime": "2022-02-07 23:59:59",
        "minmagnitude": min_magnitude,
        "orderby": "time",
    }

    response = requests.get(url, params=params)
    if not response.ok:
        raise ValueError(
            f"Something went wrong fetching earthquakes above magnitude {min_magnitude}. {response.content}"
        )

    csv = StringIO(response.text)

    return pd.read_csv(csv)


if __name__ == "__main__":
    earthquakes = get_earthquakes()
    earthquakes = upload_and_postprocess(
        earthquakes, "earthquakes", convert_to_gdf=True
    )
