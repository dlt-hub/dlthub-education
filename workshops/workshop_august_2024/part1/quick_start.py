# Import the dlt library
import dlt

# Define our data to load
data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

# Create a pipeline that loads data into DuckDB
pipeline = dlt.pipeline(
    pipeline_name="quick_start",
    destination="duckdb",
    dataset_name="mydata",
    dev_mode=True,
)

# Run the pipeline
load_info = pipeline.run(data, table_name="users")

# Print the load information
print(load_info)