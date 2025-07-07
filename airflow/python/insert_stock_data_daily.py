import psycopg2
import csv
from io import StringIO

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    "host": "host.docker.internal",
    "database": "postgres",
    "user": "postgres",
    "password": "Volubilis31*",
}

# Chemins vers les fichiers CSV
csv_file_path = '/usr/local/airflow/data/new_stock_data_prices.csv'
csv_file_path2 = '/usr/local/airflow/data/new_stock_data_volumes.csv'

table_name = 'stock_data_prices'
table_name2 = 'stock_data_volumes'

def insert_data_from_csv(file_path, table):
    with open(file_path, 'r') as f:
        csv_data = StringIO(f.read())
        reader = csv.reader(csv_data)
        next(reader)  # Sauter l'en-tête

        for row in reader:
            date = row[0]  # Supposons que la date est la première colonne
            processed_row = [None if value == '' else value for value in row]

            # Vérifier si la date existe déjà dans la table
            cursor.execute(f"SELECT 1 FROM {table} WHERE date = %s", (date,))
            if cursor.fetchone() is None:
                # Si la date n'existe pas, insérer les données
                insert_query = f"INSERT INTO {table} (date, GSPC, STOXX50E, FCHI, NASDAQ, DJI, N225) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, processed_row)

try:
    # Connexion à la base de données
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Insertion des données à partir des fichiers CSV
    insert_data_from_csv(csv_file_path, table_name)
    insert_data_from_csv(csv_file_path2, table_name2)

    # Validation des changements
    conn.commit()

except Exception as e:
    print(f"Une erreur est survenue : {e}")
    conn.rollback()

finally:
    # Fermeture de la connexion
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

print("Données insérées avec succès.")