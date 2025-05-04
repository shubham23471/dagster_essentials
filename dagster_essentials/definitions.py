import dagster as dg
from dagster_essentials.assets import metrics, trips, requests
from dagster_essentials.resources import database_resource
from dagster_essentials.jobs import trip_update_job, weekly_update_job, adhoc_request_job
from dagster_essentials.schedules import trip_update_schedule, weekly_update_schedule
from dagster_essentials.sensors import adhoc_request_sensor

# loading assets
trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])
request_assets = dg.load_assets_from_modules([requests])


# loading jobs
all_jobs = [trip_update_job, weekly_update_job, adhoc_request_job]

# loading schedules
all_schedule = [trip_update_schedule, weekly_update_schedule]

# loading sensors 
all_sensors = [adhoc_request_sensor]


# When loading a code location, Dagster looks for a variable that contains a Definitions object. 
# i.e: defs variable
defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets, *request_assets],
    resources={
        "database": database_resource,
    },
    jobs=all_jobs,
    schedules=all_schedule,
    sensors=all_sensors,

)
