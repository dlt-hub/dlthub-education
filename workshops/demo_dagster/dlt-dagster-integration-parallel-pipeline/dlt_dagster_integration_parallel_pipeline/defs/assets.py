import dlt
from dagster import AssetExecutionContext
from dagster_dlt import DagsterDltResource, dlt_assets
from dotenv import load_dotenv

from .jaffle_shop_source import dlt_source

# Standard limit for all resources
RESOURCE_LIMIT = 5


def make_resource_asset(resource_name: str):
    @dlt_assets(
        dlt_source=dlt_source.with_resources(resource_name).add_limit(RESOURCE_LIMIT),
        dlt_pipeline=dlt.pipeline(
            pipeline_name=f"jaffle_shop_{resource_name}",
            destination="duckdb",
            dataset_name="jaffle_shop_data",
            progress="log",
        ),
        name=f"jaffle_shop_{resource_name}",
        group_name="jaffle_shop",
    )
    def asset(context: AssetExecutionContext, dlt: DagsterDltResource):
        # Ensure environment variables are loaded
        load_dotenv()
        yield from dlt.run(context=context)

    return asset


resource_names = ["customers", "orders", "items", "products", "supplies"]
assets = [make_resource_asset(name) for name in resource_names]
