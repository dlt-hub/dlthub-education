from dagster import Definitions, load_assets_from_modules

from . import assets

from dagster_embedded_elt.dlt import DagsterDltResource

dlt_resource = DagsterDltResource()
all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "dlt": dlt_resource,
    },
)
