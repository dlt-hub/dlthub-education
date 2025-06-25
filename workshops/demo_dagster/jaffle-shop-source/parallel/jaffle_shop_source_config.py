def get_jaffle_shop_source_config():
    return {
        "client": {
            "base_url": "https://jaffle-shop.scalevector.ai/api/v1/"
        },
        "resource_defaults": {
            "primary_key": "id",
            "endpoint": {
                "params": {
                    "per_page": 100
                }
            }
        },
        "resources": [
            {"name": "customers", "endpoint": {"path": "customers"}},
            {"name": "orders", "endpoint": {"path": "orders"}},
            {"name": "items", "endpoint": {"path": "items"}},
            {"name": "products", "primary_key": "sku", "endpoint": {"path": "products"}},
            {"name": "supplies", "endpoint": {"path": "supplies"}},
        ]
    }

# Standard limit for all resources
RESOURCE_LIMIT = 100 