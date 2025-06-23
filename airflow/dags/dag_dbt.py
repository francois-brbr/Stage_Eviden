from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


DBT_PATH =  "/usr/local/airflow/dbt"

def load_data():
    exec(open("/usr/local/airflow/python/stock_data.py").read())

def insert_data():
    exec(open("/usr/local/airflow/python/loading_stock_prices.py").read())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG('dbt_orchestration', default_args=default_args, schedule_interval='@daily',  catchup=False) as dag:

    run_load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    ) # premiere etape du workflow : chargement des donnees

    run_insert_data = PythonOperator(
        task_id='insert_data',
        python_callable=insert_data,
    ) # seconde etape du workflow : insertion des donnees en bdd

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PATH} && dbt run --profiles-dir {DBT_PATH}",
    ) # derniere etape du workflow : script dbt > transformation de donnees et insertion en bdd

    run_load_data >> run_insert_data >> dbt_run # orchestration du workflow - maj journaliere des differents indices