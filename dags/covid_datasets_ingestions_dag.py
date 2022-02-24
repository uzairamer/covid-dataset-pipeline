from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from ingestions.covid.covid_datasets_ingestion import CovidDatasetsIngestion
from settings import DAG_FAILURE_EMAIL_LIST

args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 2, 20),
    'email': DAG_FAILURE_EMAIL_LIST,
    'email_on_failure': True,
    'email_on_retry': False,
}

with DAG('covid_datasets_ingestion',
         schedule_interval=None,
         default_args=args) as dag:
    start = DummyOperator(task_id='start')
    task = PythonOperator(
        task_id='covid_ingestion',
        python_callable=CovidDatasetsIngestion().execute
    )
    end = DummyOperator(task_id='end')

    start >> task >> end
