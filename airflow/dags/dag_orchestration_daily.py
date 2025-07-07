from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


DBT_PATH =  "/usr/local/airflow/dbt"

def load_stock_prices_daily():
    exec(open("/usr/local/airflow/python/load_stock_data_daily.py").read())

def insert_stock_prices_daily():
    exec(open("/usr/local/airflow/python/insert_stock_data_daily.py").read())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

with DAG('dag_dbt_orchestration_daily', default_args=default_args, schedule_interval=timedelta(days=1),  catchup=False) as dag:

    run_load_stock_prices_daily = PythonOperator(
        task_id='load_stock_prices_daily',
        python_callable=load_stock_prices_daily,
    ) # premiere etape du workflow : chargement des donnees provenant de diff sources

    run_insert_stock_prices_daily = PythonOperator(
        task_id='insert_stock_prices_daily',
        python_callable=insert_stock_prices_daily,
    ) # seconde etape du workflow : insertion des donnees en bdd

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PATH} && dbt run --profiles-dir {DBT_PATH}", #--models average_volume corrrelation performance
    ) # derniere etape du workflow : script dbt > transformation de donnees et insertion en bdd

    run_load_stock_prices_daily >> run_insert_stock_prices_daily >> dbt_run # orchestration du workflow - maj journaliere des differents indices