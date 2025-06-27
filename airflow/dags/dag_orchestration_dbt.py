from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


DBT_PATH =  "/usr/local/airflow/dbt"

def load_stock_prices():
    exec(open("/usr/local/airflow/python/load_stock_prices.py").read())

def insert_stock_prices():
    exec(open("/usr/local/airflow/python/insert_stock_prices.py").read())

def insert_interest_rates():
    exec(open("/usr/local/airflow/python/insert_interest_rates.py").read())

def insert_inflation_rates():
    exec(open("/usr/local/airflow/python/insert_inflation_rates.py").read())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG('dag_load_insert_dbt_orchestration', default_args=default_args, schedule_interval=None,  catchup=False) as dag:

    run_load_stock_prices = PythonOperator(
        task_id='load_stock_prices',
        python_callable=load_stock_prices,
    ) # premiere etape du workflow : chargement des donnees provenant de diff sources

    run_insert_stock_prices = PythonOperator(
        task_id='insert_stock_prices',
        python_callable=insert_stock_prices,
    ) # seconde etape du workflow : insertion des donnees en bdd 

    run_insert_interest_rates = PythonOperator(
        task_id='insert_interest_rates',
        python_callable=insert_interest_rates,
    ) # seconde etape du workflow : insertion des donnees en bdd

    run_insert_inflation_rates = PythonOperator(
        task_id='insert_inflation_rates',
        python_callable=insert_inflation_rates,
    ) # seconde etape du workflow : insertion des donnees en bdd

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PATH} && dbt run --profiles-dir {DBT_PATH}",
    ) # derniere etape du workflow : script dbt > transformation de donnees et insertion en bdd

    #run_load_stock_prices >> run_insert_stock_prices >>  run_insert_interest_rates >> run_insert_inflation_rates >>  dbt_run # orchestration du workflow - maj journaliere des differents indices
    dbt_run