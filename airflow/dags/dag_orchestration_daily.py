from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Chemin du répertoire dbt
DBT_PATH =  "/usr/local/airflow/dbt"

# Fonctions pour charger et insérer les données financières
def load_stock_prices_daily():
    exec(open("/usr/local/airflow/python/load_stock_data_daily.py").read())

def insert_stock_prices_daily():
    exec(open("/usr/local/airflow/python/insert_stock_data_daily.py").read())

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
with DAG('dag_dbt_orchestration_daily', default_args=default_args, schedule_interval=timedelta(days=1),  catchup=False) as dag:

    # Première étape du workflow : chargement des données provenant de différentes sources
    run_load_stock_prices_daily = PythonOperator(
        task_id='load_stock_prices_daily',
        python_callable=load_stock_prices_daily,
    )

    # Deuxième étape du workflow : insertion des données dans la base de données
    run_insert_stock_prices_daily = PythonOperator(
        task_id='insert_stock_prices_daily',
        python_callable=insert_stock_prices_daily,
    ) 

    # Derniere étape du workflow : éxécution du script dbt et de ses modèles
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PATH} && dbt run --profiles-dir {DBT_PATH}", # si l'on veut spéficier uniquement certains modèles ->  --models average_volume corrrelation performance
    ) 

    # Orchestration du workflow pour la mise à jour quotidienne des différents indices
    run_load_stock_prices_daily >> run_insert_stock_prices_daily >> dbt_run