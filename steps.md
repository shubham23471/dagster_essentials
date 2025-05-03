curl -LsSf https://astral.sh/uv/install.sh | sh
downloading uv 0.7.2 aarch64-apple-darwin
no checksums to verify
installing to /Users/shubham/.local/bin
  uv
  uvx
everything's installed!

To add $HOME/.local/bin to your PATH, either restart your shell or run:

    source $HOME/.local/bin/env (sh, bash, zsh)
    source $HOME/.local/bin/env.fish (fish)


1. uv init
error: Project is already initialized in `/Users/shubham/projects/learning-dagster/project-dagster-university/dagster_university/dagster_essentials` (`pyproject.toml` file exists)



export DAGSTER_HOME=/Users/shubham/projects/learning-dagster/project-dagster-university/dagster_university/dagster_essentials/dagster_home



create or replace table trips as (
    select
        VendorID as vendor_id,
        PULocationID as pickup_zone_id,
        DOLocationID as dropoff_zone_id,
        RatecodeID as rate_code_id,
        payment_type as payment_type,
        tpep_dropoff_datetime as dropoff_datetime,
        tpep_pickup_datetime as pickup_datetime,
        trip_distance as trip_distance,
        passenger_count as passenger_count,
        total_amount as total_amount
    from 'data/raw/taxi_trips_2023-03.parquet'
);
