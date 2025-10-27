from prefect import flow, task
import dlt
from prefect_github import GitHubCredentials
from prefect_gcp import GcpCredentials
import os
from prefect.task_runners import ThreadPoolTaskRunner

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
def run_resource(resource_name: str, bq_dest: dlt.destinations.bigquery):

    import github_pipeline

    source = github_pipeline.github_source.with_resources(resource_name)

    pipeline = dlt.pipeline(
        pipeline_name=f"github_remote_demo_{resource_name}",
        destination=bq_dest,
        dataset_name="demo_remote_github",
        progress="log"
    )

    info = pipeline.run(source)
    print(f"{resource_name} -> {info}")
    return info

@flow(task_runner=ThreadPoolTaskRunner(max_workers=5), log_prints=True)
def main():

    #set env variables
    set_github_pat_env()
    #create bigquery destination
    bq_dest = make_bq_destination()

    a = run_resource.submit("repos", bq_dest)
    b = run_resource.submit("contributors", bq_dest)
    c = run_resource.submit("releases", bq_dest)
    d = run_resource.submit("issues", bq_dest)
    e = run_resource.submit("forks", bq_dest)

    return a.result(), b.result(), c.result(), d.result(), e.result()

if __name__ == "__main__":
    main()