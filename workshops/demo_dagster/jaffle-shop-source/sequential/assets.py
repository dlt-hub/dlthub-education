from dagster import asset, ScheduleDefinition
import logging
import os
import json
from .jaffle_shop_bigquery_pipeline import load_jaffle_shop_data

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
    logger.info("Starting Jaffle Shop data extraction...")
    
    # Set up BigQuery credentials from the JSON file
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dlthub-sandbox-6f4b18073864.json")
    logger.info(f"Using credentials from: {credentials_path}")
    
    with open(credentials_path, 'r') as f:
        credentials = json.load(f)
    
    # Set environment variables for dlt
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID"] = credentials["project_id"]
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY"] = credentials["private_key"]
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL"] = credentials["client_email"]
    
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
