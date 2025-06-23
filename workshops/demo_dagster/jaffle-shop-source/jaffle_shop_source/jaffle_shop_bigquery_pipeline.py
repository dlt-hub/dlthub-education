import dlt
from dlt.sources.rest_api import rest_api_source


def load_jaffle_shop_data() -> None:
    """Constructs a pipeline that will load Jaffle Shop data into BigQuery.
    
    This pipeline extracts data from the Jaffle Shop API and loads it into BigQuery.
    It includes customer, product, and supply data.
    """
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

    # Add limits to the data loaded from sources 
    source.orders.add_limit(2)
    source.items.add_limit(2)
    source.products.add_limit(2)
    source.supplies.add_limit(2)
    source.customers.add_limit(2)

    # Create a pipeline with BigQuery as the destination
    pipeline = dlt.pipeline(
        pipeline_name="jaffle_shop_bigquery",
        destination="bigquery",
        dataset_name="jaffle_shop_data",
        progress="log"
    )
    
    # Run the pipeline and print the load info
    info = pipeline.run(source)
    print(info)


if __name__ == "__main__":
    try:
        load_jaffle_shop_data()
    except Exception as e:
        print(f"Error running pipeline: {str(e)}")
        raise 