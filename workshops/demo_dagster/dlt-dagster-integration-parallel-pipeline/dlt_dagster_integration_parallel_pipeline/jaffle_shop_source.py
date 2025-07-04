from dlt.sources.rest_api import rest_api_source


config = {
    "client": {"base_url": "https://jaffle-shop.scalevector.ai/api/v1/"},
    "resource_defaults": {
        "primary_key": "id",
        "endpoint": {"params": {"page_size": 10}},
    },
    "resources": [
        {"name": "customers", "endpoint": {"path": "customers"}},
        {"name": "orders", "endpoint": {"path": "orders"}},
        {"name": "items", "endpoint": {"path": "items"}},
        {
            "name": "products",
            "primary_key": "sku",
            "endpoint": {"path": "products"},
        },
        {"name": "supplies", "endpoint": {"path": "supplies"}},
    ],
}


dlt_source = rest_api_source(config)
