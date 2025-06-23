import psycopg2
import csv
from io import StringIO

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    "host": "host.docker.internal", #local
    "database": "postgres",
    "user": "postgres",
    "password": "Volubilis31*",
}

# Chemin vers le fichier .csv
csv_file_path = '/usr/local/airflow/data/interest_rates.csv'

table_name = 'interest_rates'

# Connexion à la base de données
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Création de la table
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    Date DATE,
    USA FLOAT,
    Japon FLOAT,
    France FLOAT,
    Europe FLOAT

);
"""
cursor.execute(create_table_query)
conn.commit()

clear_table_query = f"TRUNCATE TABLE {table_name};"
cursor.execute(clear_table_query)
conn.commit()

# Lecture du fichier CSV
with open(csv_file_path, 'r') as f:
    # Utilisation de StringIO pour simuler un fichier en mémoire
    csv_data = StringIO(f.read())

    # Utilisation de csv.reader pour lire le fichier CSV
    reader = csv.reader(csv_data)

    # Lecture de l'en-tête pour obtenir les noms de colonnes
    next(reader)

    # Création de la requête d'insertion
    insert_query = f"INSERT INTO {table_name} (Date, USA, Japon, France, Europe) VALUES (%s, %s, %s, %s, %s)"

    for row in reader:
        print(row)  # Print the processed row to debug
        cursor.execute(insert_query, row)


# Validation des changements
conn.commit()

# Fermeture de la connexion
cursor.close()
conn.close()

print("Données insérées avec succès.")