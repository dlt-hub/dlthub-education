from prefect import flow, task
import dlt

@task(log_prints=True)
def run_resource(resource_name: str):
    
    import github_pipeline
    # pick just one resource from your dlt source
    source = github_pipeline.github_source.with_resources(resource_name)
    # unique pipeline per resource avoids dlt state clashes
    pipeline = dlt.pipeline(
        pipeline_name=f"rest_api_github__{resource_name}",
        destination="bigquery",
        dataset_name="prefect_orc_demo",
        progress="log",
    )
    info = pipeline.run(source)
    print(f"{resource_name} -> {info}")
    return info

@flow(log_prints=True)
def main():
    
    a = run_resource("repos")
    b = run_resource("contributors")
    c = run_resource("releases")
    return a, b, c

if __name__ == "__main__":
    main.serve(name="bigquery_deployment")