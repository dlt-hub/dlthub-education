from dagster import Definitions, define_asset_job, multiprocess_executor, ScheduleDefinition
from .assets import jaffle_shop_data
from .assets_parallel import (
    bigquery_resource,
    customers_parallel,
    orders_parallel,
    items_parallel,
    products_parallel,
    supplies_parallel,
)

# Define a job that materializes the jaffle_shop_data asset
jaffle_shop_data_job = define_asset_job(
    name="jaffle_shop_data_job",
    selection=[jaffle_shop_data],
    description="Job to extract and load Jaffle Shop data into BigQuery"
)

# Define the parallel job with limited concurrency
parallel_extraction_job = define_asset_job(
    name="parallel_extraction_job",
    selection=[customers_parallel, orders_parallel, items_parallel, products_parallel, supplies_parallel],
    executor_def=multiprocess_executor.configured({"max_concurrent": 4})
)

# Add a daily schedule for both jobs
jaffle_shop_data_daily_schedule = ScheduleDefinition(
    job_name="jaffle_shop_data_job",
    cron_schedule="0 0 * * *",  # Every day at midnight
    name="jaffle_shop_data_daily_schedule",
    description="Runs the sequential extraction job every day"
)

parallel_extraction_daily_schedule = ScheduleDefinition(
    job_name="parallel_extraction_job",
    cron_schedule="0 0 * * *",  # Every day at midnight
    name="parallel_extraction_daily_schedule",
    description="Runs all parallel extraction assets every day"
)

defs = Definitions(
    assets=[
        jaffle_shop_data,
        customers_parallel,
        orders_parallel,
        items_parallel,
        products_parallel,
        supplies_parallel,
    ],
    resources={
        "bigquery": bigquery_resource
    },
    jobs=[jaffle_shop_data_job, parallel_extraction_job],
    schedules=[jaffle_shop_data_daily_schedule, parallel_extraction_daily_schedule]
)
