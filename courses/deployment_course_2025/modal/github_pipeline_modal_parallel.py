import modal

app = modal.App("run-github-pipeline-parallel")
dlt_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    'pip install "dlt[bigquery]"',
).add_local_python_source("github_pipeline")


# Define the pokemon source - this will be used by the DAG
@app.function(
    image=dlt_image,
    secrets=[modal.Secret.from_name("github-api"), modal.Secret.from_name("googlecloud-secret-bigquery")],
)
def run_pipeline(resource_name):
    import dlt
    from github_pipeline import github_source

    print("Starting pipeline setup...")
    pipeline = dlt.pipeline(
        pipeline_name=f"github_pipeline_{resource_name}",
        destination="bigquery",
        dataset_name="github_data",
    )
    print("Pipeline created.")

    load_info = pipeline.run(github_source.with_resources(resource_name))
    print("Pipeline run complete.")
    return load_info


@app.function(image=dlt_image, schedule=modal.Period(minutes=1), secrets=[modal.Secret.from_name("github-api")])
def main():
    from github_pipeline import github_source
    resources = list(github_source.resources)

    for result in run_pipeline.map(resources):
        print("Result of the main function: ", result)
