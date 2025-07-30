from datetime import timedelta
from airflow.decorators import dag

import dlt
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup
from airflow.models import Variable



# modify the default task arguments - all the tasks created for dlt pipeline will inherit it
# - set e-mail notifications
# - we set retries to 0 and recommend to use `PipelineTasksGroup` retry policies with tenacity library, you can also retry just extract and load steps
# - execution_timeout is set to 20 hours, tasks running longer that that will be terminated

default_task_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': 'test@test.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'execution_timeout': timedelta(hours=20),
}

# modify the default DAG arguments
# - the schedule below sets the pipeline to `@daily` be run each day after midnight, you can use crontab expression instead
# - start_date - a date from which to generate backfill runs
# - catchup is False which means that the daily runs from `start_date` will not be run, set to True to enable backfill
# - max_active_runs - how many dag runs to perform in parallel. you should always start with 1


@dag(
    dag_id="pokemon_dag",
    schedule_interval='@daily',
    start_date=pendulum.datetime(2023, 7, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args
)
def load_data():

    import os

    # Fetch Airflow variables and set as env vars with correct dlt naming convention
    os.environ["REST_API_POKEMON__DESTINATION__BIGQUERY__CREDENTIALS__PROJECT_ID"] = Variable.get("bigquery_project_id")
    os.environ["REST_API_POKEMON__DESTINATION__BIGQUERY__CREDENTIALS__CLIENT_EMAIL"] = Variable.get("bigquery_client_email")
    
    # Fix private key formatting - replace literal \n with actual newlines (private key has \n in it)
    private_key = Variable.get("bigquery_private_key").replace("\\n", "\n")
    os.environ["REST_API_POKEMON__DESTINATION__BIGQUERY__CREDENTIALS__PRIVATE_KEY"] = private_key
    
    # set `use_data_folder` to True to store temporary data on the `data` bucket. Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup("pipeline_decomposed", use_data_folder=False, wipe_local_data=True)

    # Import the source function from pokemon_pipeline.py
    from pokemon_pipeline import pokemon_source

    # modify the pipeline parameters 
    pipeline = dlt.pipeline(
        pipeline_name='rest_api_pokemon',
        dataset_name='pokemon_dataset',
        destination="bigquery",
        full_refresh=False # must be false if we decompose
    )
    # create the source, the "serialize" decompose option will converts dlt resources into Airflow tasks. use "none" to disable it
    tasks.add_run(
        pipeline,
        pokemon_source,
        decompose="serialize",
        trigger_rule="all_done",
        retries=0,
        provide_context=True
    )

dag = load_data()

# run: export AIRFLOW_HOME="/Users/dlthubgtm/Desktop/Aashish/Airflow Sandbox"
