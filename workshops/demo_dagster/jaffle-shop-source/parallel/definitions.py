from dagster import Definitions, define_asset_job, multiprocess_executor, ScheduleDefinition
from .assets_parallel import (
    bigquery_resource,
    customers_parallel,
    orders_parallel,
    items_parallel,
    products_parallel,
    supplies_parallel,
)

parallel_extraction_job = define_asset_job(
    name="parallel_extraction_job",
    selection=[customers_parallel, orders_parallel, items_parallel, products_parallel, supplies_parallel],
    executor_def=multiprocess_executor.configured({"max_concurrent": 4})
)
parallel_extraction_daily_schedule = ScheduleDefinition(
    job_name="parallel_extraction_job",
    cron_schedule="0 0 * * *",
    name="parallel_extraction_daily_schedule"
)

defs = Definitions(
    assets=[customers_parallel, orders_parallel, items_parallel, products_parallel, supplies_parallel],
    resources={"bigquery": bigquery_resource},
    jobs=[parallel_extraction_job],
    schedules=[parallel_extraction_daily_schedule]
) 