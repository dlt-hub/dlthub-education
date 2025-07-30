from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG("test_dag", start_date=datetime(2023,1,1), schedule_interval=None, catchup=False) as dag:
    t1 = EmptyOperator(task_id="t1")