import sqlite3
import pandas as pd

# Connexion à la base de données SQLite
connexion = sqlite3.connect("bdd.db")

# Lecture des données de la table "metrics" dans un DataFrame pandas
df = pd.read_sql_query("SELECT * FROM metrics", connexion)

# Exportation du DataFrame vers un fichier CSV
df.to_csv("metrics.csv", index=False)

# Fermeture de la connexion à la base de données SQLite
connexion.close()
