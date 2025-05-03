import dagster as dg

from dagster_essentials.assets import metrics, trips

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])

# When loading a code location, Dagster looks for a variable that contains a Definitions object. 
# i.e: defs variable
defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets],
)
