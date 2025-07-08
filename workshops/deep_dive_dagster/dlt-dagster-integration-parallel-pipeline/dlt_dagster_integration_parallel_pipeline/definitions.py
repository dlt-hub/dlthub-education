from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    multiprocess_executor,
)
from dagster_dlt import DagsterDltResource

from .defs.assets import assets

MAX_WORKERS = 5

job = define_asset_job(
    name="jaffle_shop_job",
    selection=assets,
    executor_def=multiprocess_executor.configured({"max_concurrent": MAX_WORKERS}),
)

schedule = ScheduleDefinition(
    job_name="jaffle_shop_job",
    cron_schedule="0 0 * * *",
    name="jaffle_shop_daily_schedule",
)

defs = Definitions(
    assets=assets,
    jobs=[job],
    schedules=[schedule],
    resources={"dlt": DagsterDltResource()},
)
