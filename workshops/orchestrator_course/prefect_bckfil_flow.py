import os
import dlt
import copy
from datetime import datetime, timedelta, timezone
from prefect import flow, task
from prefect.blocks.system import Secret
from prefect_github import GitHubCredentials
from prefect.task_runners import ThreadPoolTaskRunner
from dlt.sources.rest_api import rest_api_source
import example_pipeline
 

def _set_env(md_db: str):
    """
    Sets environment variables required by dlt pipelines.
    - GitHub PAT (loaded from Prefect block "github-pat") for API auth
    - MotherDuck token (loaded from Prefect block "motherduck-token") for destination auth
    - Destination DB name (MotherDuck database)
    
    Args:
        md_db (str): Name of the MotherDuck database to write into.
    """
    # GitHub PAT (GitHubCredentials.token is SecretStr -> use .get_secret_value())
    pat = GitHubCredentials.load("github-pat").token.get_secret_value()
    os.environ["SOURCES__ACCESS_TOKEN"] = pat  # dlt.secrets["sources.access_token"]
    # MotherDuck auth + DB name
    md_token = Secret.load("motherduck-token").get()
    os.environ["MOTHERDUCK_TOKEN"] = md_token
    os.environ["DESTINATION__MOTHERDUCK__CREDENTIALS__PASSWORD"] = md_token
    os.environ["DESTINATION__MOTHERDUCK__CREDENTIALS__DATABASE"] = md_db

@task(retries=2, log_prints=True)
def run_resource_in_task_pipeline(resource_name: str, md_db: str, start_date: str = None, end_date: str = None):
    """
    Runs a specific resource from the GitHub API in a dedicated task pipeline, named after the
    resource, so that each task pipeline runs in isolation.
    If resource is "forks", you can run with backfilling by setting start_date and end_date.
    
    Args:
        resource_name (str): Name of the GitHub resource to run.
        md_db (str): Name of the MotherDuck database to write into.
        start_date (str): ISO 8601 formatted start date for backfilling (for forks resource).
        end_date (str): ISO 8601 formatted end date for backfilling (for forks resource).
    """
    # Ensure environment vars for dlt are set for this task execution
    _set_env(md_db)
    # Copy pipeline config so modifications don’t leak between tasks
    config = copy.deepcopy(example_pipeline.config)
    # If the resource is "forks" and a backfill window is provided, inject it dynamically
    if resource_name == "forks" and start_date and end_date:
        for res in config["resources"]:
            if res["name"] == "forks":
                res["endpoint"]["incremental"]["initial_value"] = start_date
                res["endpoint"]["incremental"]["end_value"] = end_date
    # pick just one resource from your dlt source
    source = rest_api_source(config).with_resources(resource_name)
    # unique pipeline per resource avoids dlt state clashes
    pipeline = dlt.pipeline(
        pipeline_name=f"rest_api_github__{resource_name}",
        destination="motherduck",
        dataset_name="rest_api_data_mlt_backfill",
        progress="log",
    )
    # Run extraction + load into destination
    load_info = pipeline.run(source)
    print(f"{resource_name} -> {load_info}")
    return load_info

@flow(task_runner=ThreadPoolTaskRunner(max_workers=5), log_prints=True)
def main(md_db: str = "dlt_test"):
    """
    Main Prefect flow that runs all GitHub resources in parallel.

    Args:
        md_db (str, optional): MotherDuck database name. Defaults to "dlt_test".
    """
    # Get today's datetime in UTC and subtract one day to get yesterday's date
    # Create interval from yesterday to today
    beginning_of_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_yesterday = beginning_of_today - timedelta(days=1)

    start_iso = start_of_yesterday.isoformat()  # Outputs: 2025-08-30T00:00:00+00:00
    end_iso = beginning_of_today.isoformat() 
    
    # Launch tasks concurrently (repos, contributors, issues, forks, releases)

    a = run_resource_in_task_pipeline.submit("repos", md_db)
    b = run_resource_in_task_pipeline.submit("contributors", md_db)
    c = run_resource_in_task_pipeline.submit("issues", md_db)
    d = run_resource_in_task_pipeline.submit("forks", md_db, start_date=start_iso, end_date=end_iso)
    e = run_resource_in_task_pipeline.submit("releases", md_db)

    # Wait for all tasks to complete and return results
    return a.result(), b.result(), c.result(), d.result(), e.result()

if __name__ == "__main__":
    main()
