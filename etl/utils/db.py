"""Utility functions to interact with a PostGIS enabled Postgres database"""

import os

import geopandas as gpd
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from unidecode import unidecode

load_dotenv(override=True)

SQL_FOLDER = os.path.join(os.pardir, "sql")


def create_pg_engine():
    """Create a SQLAlchemy Postgres Engine from environment variables"""
    connection_string = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
        host=os.environ["PG_HOST"],
        port=os.environ["PG_PORT"],
        db=os.environ["PG_DATABASE"],
    )

    return create_engine(connection_string)


PG_ENGINE = create_pg_engine()


def run_query(sql_query):
    """Create a connection to the database and run a query without retrieving results

    Used for DDL statements, not fetching data
    """
    conn = PG_ENGINE.connect()
    conn.execute(sql_query)
    conn.close()


def to_db(df, table_name):
    """Upload a DataFrame or GeoDataFrame to the Postgres/PostGIS database"""
    if isinstance(df, gpd.GeoDataFrame):
        df.to_postgis(table_name, PG_ENGINE, if_exists="replace", index=False)
    elif isinstance(df, pd.DataFrame):
        df.to_sql(table_name, PG_ENGINE, if_exists="replace", index=False)
    else:
        raise ValueError(
            f'"df" must be a DataFrame or GeoDataFrame, received "{type(df)}" instead'
        )


def from_db(table_or_query):
    """Run a query against the database and retrieve results as a Pandas DataFrame"""
    return pd.read_sql(table_or_query, PG_ENGINE)


def format_column(column_name):
    """Format a column name to be a valid PG identifier"""
    chars_to_remove = "¿?(),."
    chars_to_replace = {"/": "_", " ": "_", "%": "pct"}
    for char in chars_to_remove:
        column_name = column_name.replace(char, "")
    for original_char, new_char in chars_to_replace.items():
        column_name = column_name.replace(original_char, new_char)

    # Multiple underscores into a single one
    column_name = "_".join([part for part in column_name.split("_") if part != ""])

    column_name = unidecode(column_name.lower())
    return column_name


def gdf_from_df(df):
    """Construct a GeoDataFrame from a Pandas' DataFrame

    Assume the original DataFrame contains point information
    in fields `latitude` and `longitude`
    """
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"])
    )
    gdf = gdf.drop(columns=["latitude", "longitude"])
    gdf = gdf.set_crs(epsg=4326)

    return gdf


def drop_geojson_view(table):
    """Drop a GeoJSON view of a table for use in Leaflet"""
    sql = "DROP VIEW IF EXISTS {t}_geojson".format(t=table)

    run_query(sql)


def create_geojson_view(table):
    """Create a GeoJSON view of a table for use in Leaflet"""
    with open(os.path.join(SQL_FOLDER, "table_to_geojson.sql")) as f:
        sql = f.read().format(t=table)

    run_query(sql)


def upload_and_postprocess(gdf, table_name, convert_to_gdf=False):
    """Upload a GeoDataFrame to the database and create a GeoJSON view"""
    column_lookup = {c: format_column(c) for c in gdf.columns}
    gdf = gdf.rename(columns=column_lookup)
    if convert_to_gdf:
        gdf = gdf_from_df(gdf)
    drop_geojson_view(table_name)
    to_db(gdf, table_name)

    # Also upload column name lookup
    column_df = pd.DataFrame(pd.Series(column_lookup), columns=["db"])
    column_df.index.name = "original"
    column_df = column_df.reset_index()
    to_db(column_df, f"{table_name}_keys")

    create_geojson_view(table_name)
