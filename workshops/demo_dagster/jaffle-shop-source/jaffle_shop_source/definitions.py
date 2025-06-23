from dagster import Definitions, define_asset_job
from .assets import jaffle_shop_data, jaffle_shop_hourly_schedule

# Define a job that materializes the jaffle_shop_data asset
jaffle_shop_data_job = define_asset_job(
    name="jaffle_shop_data_job",
    selection=[jaffle_shop_data],
    description="Job to extract and load Jaffle Shop data into BigQuery"
)

defs = Definitions(
    assets=[jaffle_shop_data],
    jobs=[jaffle_shop_data_job],
    schedules=[jaffle_shop_hourly_schedule]
)
