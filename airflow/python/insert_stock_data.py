import psycopg2
import csv
from io import StringIO

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    "host": "host.docker.internal", #localhost
    "database": "postgres",
    "user": "postgres",
    "password": "Eviden2025BDX**",
}

# Chemins vers les fichiers .csv
csv_file_path_price = '/usr/local/airflow/data/stock_data_prices.csv'
csv_file_path_volume = '/usr/local/airflow/data/stock_data_volumes.csv'

# Nom des tables
table_price = 'stock_data_prices'
table_volume = 'stock_data_volumes'

# Connexion à la base de données
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# ---------- Création de la table stock_data_prices -------------- #
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_price} (
    date DATE,
    GSPC FLOAT,
    STOXX50E FLOAT,
    FCHI FLOAT,
    NASDAQ FLOAT,
    DJI FLOAT,
    N225 FLOAT
);
"""
cursor.execute(create_table_query)
conn.commit()

clear_table_query = f"TRUNCATE TABLE {table_price};"
cursor.execute(clear_table_query)
conn.commit()

# ------------- Création de la table stock_data_volumes -------------- #
create_table_query2 = f"""
CREATE TABLE IF NOT EXISTS {table_volume} (
    date DATE,
    GSPC FLOAT,
    STOXX50E FLOAT,
    FCHI FLOAT,
    NASDAQ FLOAT,
    DJI FLOAT,
    N225 FLOAT
);
"""
cursor.execute(create_table_query2)
conn.commit()

clear_table_query2 = f"TRUNCATE TABLE {table_volume};"
cursor.execute(clear_table_query2)
conn.commit()

# -------------------------------------------------------------------- INSERTION PRICES ------------------------------------------------------------------------- #

with open(csv_file_path_price, 'r') as f: # Lecture du fichier "stock_data_prices.csv"
    
    csv_data = StringIO(f.read()) # Utilisation de StringIO pour simuler un fichier en mémoire

    reader = csv.reader(csv_data) # Utilisation de csv.reader pour lire le fichier CSV

    next(reader) # Lecture de l'en-tête pour obtenir les noms de colonnes

    insert_query = f"INSERT INTO {table_price} (date, GSPC, STOXX50E, FCHI, NASDAQ, DJI, N225) VALUES (%s, %s, %s, %s, %s, %s, %s)" # Création de la requête d'insertion

    for row in reader: # Insertion des données

        processed_row = [None if value == '' else value for value in row] # Remplacer les valeurs vides par None

        cursor.execute(insert_query, processed_row)

conn.commit() # Validation des changements


# -------------------------------------------------------------------- INSERTION VOLUMES --------------------------------------------------------------------------- #

with open(csv_file_path_volume, 'r') as f: # Lecture du fichier csv_file_volume
    
    csv_data = StringIO(f.read()) # Utilisation de StringIO pour simuler un fichier en mémoire

    reader = csv.reader(csv_data) # Utilisation de csv.reader pour lire le fichier CSV

    next(reader) # Lecture de l'en-tête pour obtenir les noms de colonnes

    insert_query = f"INSERT INTO {table_volume} (date, GSPC, STOXX50E, FCHI, NASDAQ, DJI, N225) VALUES (%s, %s, %s, %s, %s, %s, %s)" # Création de la requête d'insertion

    for row in reader: # Insertion des données
    
        processed_row = [None if value == '' else value for value in row] # Remplacer les valeurs vides par None afin d'éviter des erreurs

        cursor.execute(insert_query, processed_row)

conn.commit() # Validation des changements

# Fermeture de la connexion
cursor.close()
conn.close()

print("Données insérées avec succès.")