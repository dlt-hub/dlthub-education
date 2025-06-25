from dagster import Definitions, define_asset_job, ScheduleDefinition
from .assets import jaffle_shop_data

jaffle_shop_data_job = define_asset_job(name="jaffle_shop_data_job", selection=[jaffle_shop_data])
jaffle_shop_data_daily_schedule = ScheduleDefinition(
    job_name="jaffle_shop_data_job",
    cron_schedule="0 0 * * *",
    name="jaffle_shop_data_daily_schedule"
)

defs = Definitions(
    assets=[jaffle_shop_data],
    jobs=[jaffle_shop_data_job],
    schedules=[jaffle_shop_data_daily_schedule]
)
