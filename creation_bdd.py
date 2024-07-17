import sqlite3

connexion=sqlite3.connect("bdd.db")
curseur=connexion.cursor()

curseur.execute("DROP TABLE IF EXISTS metrics")
curseur.execute(""" CREATE TABLE  metrics(
                    nom_modele INT INCREMENTAL  PRIMARY KEY,
                    mae FLOAT,
                    mse FLOAT,
                    r2 FLOAT
        
                )
                """)