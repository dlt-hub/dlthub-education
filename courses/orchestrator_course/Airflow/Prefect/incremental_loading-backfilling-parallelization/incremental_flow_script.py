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
def run_resource(resource_name: str, bq_dest: dlt.destinations.bigquery, incremental_date: str = None):

    import github_pipeline

    base_source = github_pipeline.github_source
    selected_source = base_source.with_resources(resource_name)

    #apply incremental loading to only issues resource
    if incremental_date:
        selected_source.apply_hints(
            incremental=dlt.sources.incremental(
                "created_at",
                initial_value=incremental_date
            )
        )


    pipeline = dlt.pipeline(
        pipeline_name=f"github_inc_demo_{resource_name}",
        destination=bq_dest,
        dataset_name="demo_inc_github",
        progress="log"
    )

    info = pipeline.run(selected_source)
    print(f"{resource_name} -> {info}")
    return info

@flow(log_prints=True)
def main(incremental_date: str | None = None):

    #set env variables
    set_github_pat_env()
    #create bigquery destination
    bq_dest = make_bq_destination()

    a = run_resource("repos", bq_dest)
    b = run_resource("contributors", bq_dest)
    c = run_resource("releases", bq_dest)
    d = run_resource("issues", bq_dest, incremental_date=incremental_date)

    return a, b, c, d

if __name__ == "__main__":
    main()