from dagster import asset, ScheduleDefinition
import logging
import os
import json
from .jaffle_shop_bigquery_pipeline import load_jaffle_shop_data
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asset(
    description="Extract and load Jaffle Shop data into BigQuery",
    group_name="jaffle_shop",
    key_prefix=["jaffle_shop", "raw"]
)
def jaffle_shop_data() -> None:
    """Extract data from Jaffle Shop API and load it into BigQuery."""
    # Ensure environment variables are loaded
    load_dotenv()
    logger.info("Starting Jaffle Shop data extraction...")
    credentials = {
        "project_id": os.getenv("DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID"),
        "private_key": os.getenv("DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY"),
        "client_email": os.getenv("DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL")
    }
    logger.info(f"Using credentials from environment variables")
    # Run the pipeline
    load_jaffle_shop_data()
    logger.info("Data load completed successfully")

# Define a schedule that runs every hour
jaffle_shop_hourly_schedule = ScheduleDefinition(
    job_name="jaffle_shop_data_job",  # This will be the job that runs the asset
    cron_schedule="0 * * * *",  # Run at the top of every hour
    name="jaffle_shop_hourly_schedule",
    description="Runs Jaffle Shop data pipeline every hour"
)
