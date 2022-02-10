"""Global Volcanism Program (Smithsonian, 2013)

World volcanoes can be searched and downloaded as an XML from the Smithsonian Instituion's
[Global Volcanism Program](https://volcano.si.edu/). XML downloads as a non-standard `.xls`
file which we parse here directly using Beautiful Soup.

Volcanoes are downloaded by country since the general XML download only retrieves a sample
of 44 volcanoes. Only Holocene volcanoes are taken into account.

More than 12k results appear for only 1346 unique Holocene volcanoes.
Most are attributes (cone, etc). We'll keep only the main register
(where country and other fields are not null)

Not available for commercial use! [Terms Of Use](https://volcano.si.edu/gvp_termsofuse.cfm)
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from utils.db import upload_and_postprocess


def get_country_list():
    """Get a list of possible countries from the Volcano Search page"""
    country_list_url = "https://volcano.si.edu/search_volcano.cfm"
    country_list_html = BeautifulSoup(
        requests.get(country_list_url).text, features="html.parser"
    )

    country_list = country_list_html.find_all(attrs={"id": "multidrop3"})[0]
    countries = [country.attrs["value"] for country in country_list.find_all("option")]

    return countries


def get_country_xml(country_name):
    """Get the XML of an individual country. Most fields may be an empty string"""
    post_fields = [
        "volcano",
        "pop_num",
        "pop_range",
        "photos",
        "emissions",
        "deformation",
        "polygon",
        "rock_types[]",
        "feature_types[]",
        "evidence_level[]",
        "volcano_type[]",
    ]
    post_data = {f: "" for f in post_fields}
    post_data["country[]"] = country_name

    country_excel_url = "https://volcano.si.edu/database/search_volcano_excel.cfm"
    response = requests.post(country_excel_url, data=post_data)
    if not response.ok:
        raise ValueError(
            f'Something went wrong requesting data from country "{country_name}". {response.content}'
        )

    return BeautifulSoup(response.text, features="lxml")


def parse_country_xml(country_xml):
    """Convert a country XML to a Pandas DataFrame

    First row may be ignored. Second contains a header, following ones contain
    individual volcanoes. If many table are present, use just the first one
    """
    # Ignore first row. Second contains header, next contain individual volcanoes
    rows = country_xml.find_all("table")[0]("row")
    column_names = [cell.text for cell in rows[1].find_all("cell")]
    data_rows = rows[2:]
    vals = []
    for row in data_rows:
        vals.append([cell.text for cell in row.find_all("cell")])

    return pd.DataFrame(vals, columns=column_names)


if __name__ == "__main__":
    countries = get_country_list()

    country_dfs = []
    for country in tqdm(countries):
        country_xml = get_country_xml(country)
        country_dfs.append(parse_country_xml(country_xml))

    volcanoes = pd.concat(country_dfs, ignore_index=True)
    volcanoes = volcanoes.loc[
        (volcanoes["Country"].notnull()) & (volcanoes["Longitude"] != "")
    ]  # Keep just main rows, no attributes. Remove "Unknown" row

    upload_and_postprocess(volcanoes, "volcanoes", convert_to_gdf=True)
