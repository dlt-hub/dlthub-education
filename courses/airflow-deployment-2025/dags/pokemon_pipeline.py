import dlt
from dlt.sources.rest_api import rest_api_source

# Define the pokemon source - this will be used by the DAG
pokemon_source = rest_api_source(
    {
        "client": {
            "base_url": "https://pokeapi.co/api/v2/"
        },
        "resource_defaults": {
            "endpoint": {
                "params": {
                    "limit": 1000,
                },
            },
        },
        "resources": [
            "pokemon",
            "berry",
            "location",
            "move",
            "machine"
        ],
    }
)

# Only run the pipeline if this script is executed directly
if __name__ == "__main__":
    print("Starting pipeline setup...")
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_pokemon_3",
        destination="bigquery", #dlt.destinations.duckdb(destination_name="pokemon_hahaha.duckdb")
        dataset_name="pokemon_dataset_3",
    )
    print("Pipeline created.")
    print("Pokemon source created.")

    load_info = pipeline.run(pokemon_source)
    print("Pipeline run complete.")
    print("Load info:", load_info)
