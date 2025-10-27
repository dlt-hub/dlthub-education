from prefect import flow, task
import dlt
from prefect_github import GitHubCredentials
from prefect_gcp import GcpCredentials
import os

def set_github_pat_env():

    pat = GitHubCredentials.load("github-pat").token.get_secret_value()
    os.environ["SOURCES__ACCESS_TOKEN"] = pat 

def make_bq_destination():

    #get service account info
    gcp = GcpCredentials.load("gcp-creds")
    creds = gcp.service_account_info.get_secret_value() or {}
    #get project id
    project = creds.get("project_id")
    #create a bigquery destination
    return dlt.destinations.bigquery(credentials=creds, project_id=project)


@task(log_prints=True)
def run_resource(resource_name: str, bq_dest: dlt.destinations.bigquery, start_date: str = None, end_date: str = None):

    import github_pipeline

    base_source = github_pipeline.github_source

    #apply backfilling to only forks resource
    if resource_name == "forks" and start_date and end_date:
        base_source.forks.apply_hints(
            incremental=dlt.sources.incremental(
                "created_at",
                initial_value=start_date,
                end_value=end_date,
                row_order="asc"
            )
        )

    selected_source = base_source.with_resources(resource_name)

    pipeline = dlt.pipeline(
        pipeline_name=f"github_bckfill_demo_{resource_name}",
        destination=bq_dest,
        dataset_name="demo_backfill_github",
        progress="log"
    )

    info = pipeline.run(selected_source)
    print(f"{resource_name} -> {info}")
    return info

@flow(log_prints=True)
def main(start_date: str | None = None, end_date: str | None = None):

    #set env variables
    set_github_pat_env()
    #create bigquery destination
    bq_dest = make_bq_destination()

    a = run_resource("repos", bq_dest)
    b = run_resource("forks", bq_dest, start_date=start_date, end_date=end_date)
    
    return a, b

if __name__ == "__main__":
    main()