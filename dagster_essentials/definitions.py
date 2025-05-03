import dagster as dg

from dagster_essentials.assets import metrics, trips
from dagster_essentials.resources import database_resource

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])

# When loading a code location, Dagster looks for a variable that contains a Definitions object. 
# i.e: defs variable
defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets],
    resources={
        "database": database_resource,
    },
)
