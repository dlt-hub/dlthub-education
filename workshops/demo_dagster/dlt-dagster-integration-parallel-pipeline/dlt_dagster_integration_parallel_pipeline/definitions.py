from dagster import Definitions, define_asset_job, ScheduleDefinition, multiprocess_executor
from dagster_dlt import DagsterDltResource
from .assets import assets

parallel_job = define_asset_job(
    name="jaffle_shop_parallel_job",
    selection=assets,
    executor_def=multiprocess_executor.configured({"max_concurrent": 3})
)

parallel_schedule = ScheduleDefinition(
    job_name="jaffle_shop_parallel_job",
    cron_schedule="0 0 * * *",
    name="jaffle_shop_parallel_daily_schedule"
)

defs = Definitions(
    assets=assets,
    jobs=[parallel_job],
    schedules=[parallel_schedule],
    resources={"dlt": DagsterDltResource()}
)