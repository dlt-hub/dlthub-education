import modal
from datetime import datetime

app = modal.App("run-github-pipeline")
dlt_image = modal.Image.debian_slim(python_version="3.12").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    'pip install "dlt[duckdb]"',
    'pip install "dlt[bigquery]"',
).add_local_python_source("github_pipeline")

# Define the pokemon source - this will be used by the DAG
@app.function(
    image=dlt_image,
    secrets=[modal.Secret.from_name("github-api"), modal.Secret.from_name("googlecloud-secret-bigquery")],
    schedule=modal.Period(minutes=1),

)
def run_pipeline(start_date: str| None = None, end_date: str | None = None):

    import dlt
    from github_pipeline import github_source

    print("Starting pipeline setup...")
    pipeline = dlt.pipeline(
        pipeline_name="github_pipeline",
        destination="bigquery",
        dataset_name="alena_github_data",
    )
    print("Pipeline created.")

    if start_date and end_date:
        # Backfilling
        github_source.forks.apply_hints(
            incremental=dlt.sources.incremental(
                "created_at",
                initial_value=start_date,
                end_value=end_date,
                row_order="asc"
            )
        )

    load_info = pipeline.run(github_source, write_disposition="replace")
    print("Pipeline run complete.")
    print("Load info:", load_info)

    dataset = pipeline.dataset()
    forks_df = dataset.forks.df()
    print(forks_df.loc[:, "created_at"].min(), forks_df.loc[:, "created_at"].max())

    if start_date and end_date:
        assert forks_df.loc[:, "created_at"].min() >= datetime.fromisoformat(start_date), forks_df.loc[:, "created_at"].min()
        assert forks_df.loc[:, "created_at"].max() <= datetime.fromisoformat(end_date), forks_df.loc[:, "created_at"].max()

    return load_info


# Only run the pipeline if this script is executed directly
@app.local_entrypoint()
def main(start_date: str| None = None, end_date: str | None = None):
    run_pipeline.remote(start_date, end_date)
