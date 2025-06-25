import dlt
from dagster import asset, ResourceDefinition
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import json
from .jaffle_shop_parallel_pipeline import source

def setup_bigquery_credentials():
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dlthub-sandbox-6f4b18073864.json")
    with open(credentials_path, 'r') as f:
        credentials = json.load(f)
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID"] = credentials["project_id"]
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY"] = credentials["private_key"]
    os.environ["DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL"] = credentials["client_email"]
    return credentials

def init_bigquery_dataset(context):
    """Initialize BigQuery dataset if it doesn't exist"""
    credentials = setup_bigquery_credentials()
    creds = service_account.Credentials.from_service_account_info(credentials)
    client = bigquery.Client(project=credentials["project_id"], credentials=creds)
    dataset_id = f"{credentials['project_id']}.jaffle_shop_data_parallel"
    try:
        client.get_dataset(dataset_id)
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)
    return client

# Define BigQuery resource
bigquery_resource = ResourceDefinition(
    resource_fn=init_bigquery_dataset,
    description="BigQuery client with dataset initialization"
)

def run_resource_pipeline(resource, pipeline_name):
    setup_bigquery_credentials()
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination="bigquery",
        dataset_name="jaffle_shop_data_parallel",
        progress="log"
    )
    pipeline.run(resource)

@asset(required_resource_keys={"bigquery"})
def customers_parallel(context):
    run_resource_pipeline(source.customers, "customers_parallel")

@asset(required_resource_keys={"bigquery"})
def orders_parallel(context):
    run_resource_pipeline(source.orders, "orders_parallel")

@asset(required_resource_keys={"bigquery"})
def items_parallel(context):
    run_resource_pipeline(source.items, "items_parallel")

@asset(required_resource_keys={"bigquery"})
def products_parallel(context):
    run_resource_pipeline(source.products, "products_parallel")

@asset(required_resource_keys={"bigquery"})
def supplies_parallel(context):
    run_resource_pipeline(source.supplies, "supplies_parallel") 