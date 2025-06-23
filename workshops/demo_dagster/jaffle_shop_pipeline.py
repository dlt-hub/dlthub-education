import dlt
from dlt.sources.rest_api import rest_api_source

# Build the REST API config
source = rest_api_source({
    "client": {
        "base_url": "https://jaffle-shop.scalevector.ai/api/v1/"
    },
    "resource_defaults": {
        "primary_key": "id",
        "endpoint": {
            "params": {
                "per_page": 500,  # Limit to 500 items per endpoint
            }
        }
    },
    "resources": [
        {
            "name": "customers",
            "endpoint": {
                "path": "customers"
            }
        },
        {
            "name": "orders",
            "endpoint": {
                "path": "orders"
            }
        },
        {
            "name": "items",
            "endpoint": {
                "path": "items"
            }
        },
        {
            "name": "products",
            "endpoint": {
                "path": "products"
            },
            "primary_key": "sku"  # Products use sku as primary key
        },
        {
            "name": "supplies",
            "endpoint": {
                "path": "supplies"
            }
        }
    ]
})

if __name__ == "__main__":
    source.orders.add_limit(2)
    source.items.add_limit(2)
    source.products.add_limit(2)
    source.supplies.add_limit(2)
    source.customers.add_limit(2)
    pipeline = dlt.pipeline(
        pipeline_name="jaffle_shop",
        destination="duckdb",
        dataset_name="jaffle_shop_data",
        progress="log"
    )
    pipeline.run(source) 