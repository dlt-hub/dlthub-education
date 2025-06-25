import dlt
from dlt.sources.rest_api import rest_api_source
from .jaffle_shop_source_config import get_jaffle_shop_source_config, RESOURCE_LIMIT


def load_jaffle_shop_data() -> None:
    """Constructs a pipeline that will load Jaffle Shop data into BigQuery.
    
    This pipeline extracts data from the Jaffle Shop API and loads it into BigQuery.
    It includes customer, product, and supply data.
    """
    # Build the REST API config
    source = rest_api_source(get_jaffle_shop_source_config())

    # Add limits to the data loaded from sources 
    source.customers.add_limit(RESOURCE_LIMIT)
    source.orders.add_limit(RESOURCE_LIMIT)
    source.items.add_limit(RESOURCE_LIMIT)
    source.products.add_limit(RESOURCE_LIMIT)
    source.supplies.add_limit(RESOURCE_LIMIT)

    # Create a pipeline with BigQuery as the destination
    pipeline = dlt.pipeline(
        pipeline_name="jaffle_shop_bigquery",
        destination="bigquery",
        dataset_name="jaffle_shop_data_with_integration",
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