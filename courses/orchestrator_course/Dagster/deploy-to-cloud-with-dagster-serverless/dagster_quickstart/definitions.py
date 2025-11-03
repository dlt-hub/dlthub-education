from .defs.assets_parallel import dagster_github_assets_parallel # change to match our asset 
from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition, multiprocess_executor # import other items for scheduling
from dagster_embedded_elt.dlt import DagsterDltResource


# create a job 
job = define_asset_job(
    name="github_job",
    selection=dagster_github_assets_parallel, # must be in the form of a list
    executor_def=multiprocess_executor.configured({"max_concurrent": 5}), # set to 5 since we have 5 endpoints
)

# create a schedule
schedule = ScheduleDefinition(
    job_name="github_job",
    cron_schedule="0 0 * * *", # run everyday,
    name="github_daily_schedule", # parameter name is just "name"
)


# modify the definitions to include the job and the schedule
defs = Definitions(
    jobs= [job], # parameter name is "jobs"
    assets=dagster_github_assets_parallel,
    resources={
    "dlt": DagsterDltResource(),
    },
    schedules=[schedule]
)