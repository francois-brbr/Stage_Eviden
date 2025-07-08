from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Chemin du répertoire dbt
DBT_PATH =  "/usr/local/airflow/dbt"

# Fonctions pour charger et insérer les données financières
def load_stock_prices():
    exec(open("/usr/local/airflow/python/load_stock_data.py").read())

def insert_stock_prices():
    exec(open("/usr/local/airflow/python/insert_stock_data.py").read())

def insert_interest_rates():
    exec(open("/usr/local/airflow/python/insert_interest_rates.py").read())

def insert_inflation_rates():
    exec(open("/usr/local/airflow/python/insert_inflation_rates.py").read())

# Paramètres du DAG Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

# Mise en place du DAG pour l'orchestration
with DAG('dag_load_insert_dbt_orchestration', default_args=default_args, schedule_interval=None,  catchup=False) as dag:

    # Première étape du workflow : chargement des données provenant de différentes sources
    run_load_stock_prices = PythonOperator(
        task_id='load_stock_prices',
        python_callable=load_stock_prices,
    )

    # Deuxième étape du workflow : insertion des données dans la base de données
    run_insert_stock_prices = PythonOperator(
        task_id='insert_stock_prices',
        python_callable=insert_stock_prices,
    )

    # Idem 
    run_insert_interest_rates = PythonOperator(
        task_id='insert_interest_rates',
        python_callable=insert_interest_rates,
    )

    # Idem 
    run_insert_inflation_rates = PythonOperator(
        task_id='insert_inflation_rates',
        python_callable=insert_inflation_rates,
    ) 

    # Derniere étape du workflow : éxécution du script dbt et de ses modèles
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PATH} && dbt run --profiles-dir {DBT_PATH}",
    )

        # Orchestration du workflow pour l'insertion des différentes données financières
    run_load_stock_prices >> run_insert_stock_prices >>  run_insert_interest_rates >> run_insert_inflation_rates >>  dbt_run 