from dagster_dlt import dlt_assets, DagsterDltResource
from dagster import AssetExecutionContext
import dlt
from .jaffle_shop_source_config import get_jaffle_shop_source_config, RESOURCE_LIMIT
from dotenv import load_dotenv

# Build the dlt source
from dlt.sources.rest_api import rest_api_source

def jaffle_shop_source():
    source = rest_api_source(get_jaffle_shop_source_config())
    source.customers.add_limit(RESOURCE_LIMIT)
    source.orders.add_limit(RESOURCE_LIMIT)
    source.items.add_limit(RESOURCE_LIMIT)
    source.products.add_limit(RESOURCE_LIMIT)
    source.supplies.add_limit(RESOURCE_LIMIT)
    return source

# Define the dlt pipeline
jaffle_shop_pipeline = dlt.pipeline(
    pipeline_name="jaffle_shop_bigquery",
    destination="bigquery",
    dataset_name="jaffle_shop_data_integration_sequential",
    progress="log"
)

@dlt_assets(
    dlt_source=jaffle_shop_source(),
    dlt_pipeline=jaffle_shop_pipeline,
    name="jaffle_shop",
    group_name="jaffle_shop",
)
def jaffle_shop_dlt_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    # Ensure environment variables are loaded
    load_dotenv()
    yield from dlt.run(context=context)
