from dagster import Definitions, define_asset_job, ScheduleDefinition
from dagster_dlt import DagsterDltResource
from .assets import jaffle_shop_dlt_assets

# Define a job for the dlt asset
jaffle_shop_dlt_job = define_asset_job(name="jaffle_shop_dlt_job", selection=[jaffle_shop_dlt_assets])

# Define a daily schedule for the job
jaffle_shop_dlt_daily_schedule = ScheduleDefinition(
    job_name="jaffle_shop_dlt_job",
    cron_schedule="0 0 * * *",
    name="jaffle_shop_dlt_daily_schedule"
)

defs = Definitions(
    assets=[jaffle_shop_dlt_assets],
    jobs=[jaffle_shop_dlt_job],
    schedules=[jaffle_shop_dlt_daily_schedule],
    resources={"dlt": DagsterDltResource()}
)
