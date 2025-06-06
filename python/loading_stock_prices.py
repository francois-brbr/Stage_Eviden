import psycopg2
import csv
from io import StringIO

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Volubilis31*",
}

# Chemin vers le fichier .csv
csv_file_path = '../data/stock_data_prices.csv'

table_name = 'stock_data'

# Connexion à la base de données
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Création de la table
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
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

# Lecture du fichier CSV
with open(csv_file_path, 'r') as f:
    # Utilisation de StringIO pour simuler un fichier en mémoire
    csv_data = StringIO(f.read())

    # Utilisation de csv.reader pour lire le fichier CSV
    reader = csv.reader(csv_data)

    # Lecture de l'en-tête pour obtenir les noms de colonnes
    next(reader)

    # Création de la requête d'insertion
    insert_query = f"INSERT INTO {table_name} (date, GSPC, STOXX50E, FCHI, NASDAQ, DJI, N225) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    # Insertion des données
    for row in reader:
        # Remplacer les valeurs vides par None
        processed_row = [None if value == '' else value for value in row]

        cursor.execute(insert_query, processed_row)

# Validation des changements
conn.commit()

# Fermeture de la connexion
cursor.close()
conn.close()

print("Données insérées avec succès.")