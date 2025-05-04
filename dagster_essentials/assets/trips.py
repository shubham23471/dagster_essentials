import requests
from dagster_essentials.assets import constants
import dagster as dg
# import duckdb 
import os
from dagster._utils.backoff import backoff
from dagster_duckdb import DuckDBResource
from dagster_essentials.partitions import monthly_partition


@dg.asset(
        partitions_def=monthly_partition
)
def taxi_trips_file(context: dg.AssetExecutionContext) -> None:
    """
      The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal.
    """
    partition_date_str = context.partition_key
    month_to_fetch = partition_date_str[:-3] # to get YYYY-MM
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as output_file:
        output_file.write(raw_trips.content)

@dg.asset
def taxi_zones_file() -> None:
    """
      The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal.
    """
    raw_taxi_zones = requests.get(
        "https://community-engineering-artifacts.s3.us-west-2.amazonaws.com/dagster-university/data/taxi_zones.csv"
    )

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(raw_taxi_zones.content)


# database: DuckDBResource => This type hint  is required to tell Dagster that the
#  dependency is a resource and not an asset.
# DuckDBResource also handles the backoff functionality
@dg.asset(
  deps=["taxi_trips_file"],
  partitions_def=monthly_partition,
)
def taxi_trips(context: dg.AssetExecutionContext, database: DuckDBResource) -> None:
  """
    The raw taxi trips dataset, loaded into a DuckDB database, partitioned by month.
  """

  partition_date_str = context.partition_key
  month_to_fetch = partition_date_str[:-3]

  query = f"""
    create table if not exists trips (
      vendor_id integer, pickup_zone_id integer, dropoff_zone_id integer,
      rate_code_id double, payment_type integer, dropoff_datetime timestamp,
      pickup_datetime timestamp, trip_distance double, passenger_count double,
      total_amount double, partition_date varchar
    );

    delete from trips where partition_date = '{month_to_fetch}';

    insert into trips
    select
      VendorID, PULocationID, DOLocationID, RatecodeID, payment_type, tpep_dropoff_datetime,
      tpep_pickup_datetime, trip_distance, passenger_count, total_amount, '{month_to_fetch}' as partition_date
    from '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)}';
  """

  with database.get_connection() as conn:
      conn.execute(query)


@dg.asset(
    deps=["taxi_zones_file"]
)
def taxi_zones(database: DuckDBResource) -> None:
    query = f"""
        create or replace table zones as (
            select
                LocationID as zone_id,
                zone,
                borough,
                the_geom as geometry
            from '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """
    with database.get_connection() as conn:
        conn.execute(query)
    

