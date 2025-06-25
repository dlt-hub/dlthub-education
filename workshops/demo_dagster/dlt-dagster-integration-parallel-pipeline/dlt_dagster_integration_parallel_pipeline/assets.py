from dotenv import load_dotenv
load_dotenv()  # Ensures .env credentials are loaded

from dagster_dlt import dlt_assets, DagsterDltResource
from dagster import AssetExecutionContext
import dlt
from .jaffle_shop_source_config import get_jaffle_shop_source_config, RESOURCE_LIMIT
from dlt.sources.rest_api import rest_api_source

def make_resource_source(resource_name):
    config = get_jaffle_shop_source_config()
    config["resources"] = [r for r in config["resources"] if r["name"] == resource_name]
    source = rest_api_source(config)
    getattr(source, resource_name).add_limit(RESOURCE_LIMIT)
    return source

def make_resource_asset(resource_name):
    pipeline = dlt.pipeline(
        pipeline_name=f"jaffle_shop_{resource_name}_bigquery",
        destination="bigquery",
        dataset_name="jaffle_shop_data_integration_parallel",
        progress="log"
    )
    @dlt_assets(
        dlt_source=make_resource_source(resource_name),
        dlt_pipeline=pipeline,
        name=f"jaffle_shop_{resource_name}",
        group_name="jaffle_shop",
    )
    def asset(context: AssetExecutionContext, dlt: DagsterDltResource):
        yield from dlt.run(context=context)
    return asset

resource_names = ["customers", "orders", "items", "products", "supplies"]
assets = [make_resource_asset(name) for name in resource_names]

# Optionally, expose them individually for import
customers_asset, orders_asset, items_asset, products_asset, supplies_asset = assets
