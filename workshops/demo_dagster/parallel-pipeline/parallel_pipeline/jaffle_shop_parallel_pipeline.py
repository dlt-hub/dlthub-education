import dlt
from dlt.sources.rest_api import rest_api_source
from .jaffle_shop_source_config import get_jaffle_shop_source_config, RESOURCE_LIMIT

config = get_jaffle_shop_source_config()
source = rest_api_source(config)

# Set a limit for each resource
source.customers.add_limit(RESOURCE_LIMIT)
source.orders.add_limit(RESOURCE_LIMIT)
source.items.add_limit(RESOURCE_LIMIT)
source.products.add_limit(RESOURCE_LIMIT)
source.supplies.add_limit(RESOURCE_LIMIT)