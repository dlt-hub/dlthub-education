import os
import dlt
from prefect import flow, task
from prefect_github import GitHubCredentials
from prefect_gcp import GcpCredentials

def set_github_pat_env():
    # GitHub PAT (GitHubCredentials.token is SecretStr -> use .get_secret_value())
    pat = GitHubCredentials.load("github-pat").token.get_secret_value() 
    os.environ["SOURCES__ACCESS_TOKEN"] = pat # dlt.secrets["sources.access_token"]
    
def make_bq_destination():
    #get service account info from gcp credentials block
    gcp = GcpCredentials.load("gcp-creds")
    creds = gcp.service_account_info.get_secret_value() or {}
    #get project id from service account info
    project = creds.get("project_id")
    #create bigquery destination
    return dlt.destinations.bigquery(credentials=creds, project_id=project)

@task(log_prints=True)
def run_resource(resource_name: str, bq_dest: dlt.destinations.bigquery):
    
    import github_pipeline
    # pick just one resource from your dlt source
    source = github_pipeline.github_source.with_resources(resource_name)
    # unique pipeline per resource avoids dlt state clashes
    pipeline = dlt.pipeline(
        pipeline_name=f"rest_api_github__{resource_name}",
        destination=bq_dest,
        dataset_name="prefect_orc_demo",
        progress="log",
    )
    info = pipeline.run(source)
    print(f"{resource_name} -> {info}")
    return info

@flow(log_prints=True)
def main():
    #set env variables
    set_github_pat_env()
    #create bigquery destination
    bq_dest = make_bq_destination()
    #run resources
    a = run_resource("repos", bq_dest)
    b = run_resource("contributors", bq_dest)
    c = run_resource("releases", bq_dest)
    return a, b, c

if __name__ == "__main__":
    main()