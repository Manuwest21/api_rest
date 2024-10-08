from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, constr, validator
import pickle
import pandas as pd
import joblib
import os
from securite import has_access
import mlflow
from typing import Dict, Any
import sqlite3
from sklearn.metrics import mean_squared_error, r2_score
from fastapi import HTTPException
from typing import Dict, Any
from typing import Annotated
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
import subprocess
# import sentry_sdk

# Charger le pipeline depuis le fichier
# pipe = joblib.load('pipeline_model.joblib')
# Créer une classe pour les données d'entrée
# sentry_sdk.init(
#     dsn="https://29402a8f399496504f9eb69c6453a0a6@o4507447356620800.ingest.de.sentry.io/4508039867859024",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for tracing.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
# )


file_path_pkl = os.path.join('construction_modèle_Ml', 'modele_4_ml.pkl')
file_path_joblib=os.path.join('construction_modèle_Ml', 'pipeline_model.joblib')



class LengthConstraint:
    def __init__(self, min_length: int, max_length: int):
        self.min_length = min_length
        self.max_length = max_length

class RangeConstraint:
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
# définition de la class BaseModel, implémentation de limitations pour garantir la validation des données et réduire les risques de sécurité.
# class InputData(BaseModel):
#     country: Annotated[str, LengthConstraint(1, 15)]
#     genre: Annotated[str, LengthConstraint(1, 15)]
#     public: Annotated[str, LengthConstraint(1, 15)]
#     distributeur: Annotated[str, LengthConstraint(1, 15)]
    
#     numero_semaine: Annotated[int, RangeConstraint(1, 52)]
#     durée: Annotated[int, RangeConstraint(60, 300)]
    
#     directeur: Annotated[str, LengthConstraint(1, 30)]
#     acteur1: Annotated[str, LengthConstraint(1, 30)]
#     acteur2: Annotated[str, LengthConstraint(1, 30)]
#     acteur3: Annotated[str, LengthConstraint(1, 30)]
        

class donnees_film(BaseModel):
    country: str
    genre: str
    public: str
    distributeur: str
    numero_semaine: int
    durée: int
    directeur: str
    acteur1: str
    acteur2: str
    acteur3: str

    @validator('country', 'genre', 'public', 'distributeur', 'directeur', 'acteur1', 'acteur2', 'acteur3')
    def check_length(cls, v):
        if len(v) < 1 or len(v) > 25:
            raise ValueError('La longueur de ce type de donnée ne dépasse pas 25 caractéres')
        return v

    @validator('numero_semaine')
    def check_numero_semaine(cls, v):
        if v < 1 or v > 52:
            raise ValueError('les numeros de semaine sont compris entre 1 et 52')
        return v

    @validator('durée')
    def check_durée(cls, v):
        if v < 60 or v > 300:
            raise ValueError('la durée de film est ente 60 et 300 minutes')
        return v
    

    
###111#
# Charger le modèle pickle
with open('modele_4_ml.pkl', 'rb') as f:
    model = pickle.load(f)
pipe = joblib.load(file_path_joblib)
# Créer un routeur pour les endpoints de modelisation1
router = APIRouter()
def get_db_connection():
    try:
        conn = sqlite3.connect('predictions.db')
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")




# Définition d'une route pour effectuer des prédictions, on va se référer à celle-ci en accédant à l'interface mlflow pour suivre les performances en temps réel. 

from fastapi import HTTPException, Depends
import pandas as pd
import mlflow
import sqlite3

# Compteur global pour les prédictions: pour faire tourner le fichier drift toutes les 3 prédictions
prediction_counter = 0

mlflow.set_experiment("visualisation_predictions_cinema")
mlflow.set_tracking_uri('mlruns')

# @router.post("/predict_film/", response_model=donnees_film, dependencies=[Depends(has_access)])
# def predict_film(
#     country: str = Query(..., description="Pays d'origine du film (1-25 caractères)"),
#     genre: str = Query(..., description="Genre du film (1-25 caractères)"),
#     public: str = Query(..., description="Public cible (1-25 caractères)"),
#     distributeur: str = Query(..., description="Nom du distributeur (1-25 caractères)"),
#     numero_semaine: int = Query(..., description="Numéro de la semaine (1-52)", example=12),
#     duree: int = Query(..., description="Durée du film en minutes (60-300)", example=120),
#     directeur: str = Query(..., description="Nom du réalisateur (1-25 caractères)"),
#     acteur1: str = Query(..., description="Premier acteur (1-25 caractères)"),
#     acteur2: str = Query(..., description="Deuxième acteur (1-25 caractères)"),
#     acteur3: str = Query(..., description="Troisième acteur (1-25 caractères)")
# ):
#     """
#     Cet endpoint permet de faire une prédiction basée sur les caractéristiques d'un film.
    
#     L'utilisateur doit fournir :
#     - Le pays d'origine du film (country).
#     - Le genre du film (genre).
#     - Le public cible (public).
#     - Le distributeur (distributeur).
#     - Le numéro de la semaine (numero_semaine) entre 1 et 52.
#     - La durée du film (duree) en minutes.
#     - Les trois principaux acteurs (acteur1, acteur2, acteur3).
#     """
    
#     # Créer le dataframe pour les données d'entrée
#     input_data = donnees_film(
#         country=country,
#         genre=genre,
#         public=public,
#         distributeur=distributeur,
#         numero_semaine=numero_semaine,
#         durée=duree,
#         directeur=directeur,
#         acteur1=acteur1,
#         acteur2=acteur2,
#         acteur3=acteur3
#     )

#     # Charger et exécuter le modèle de prédiction
#     try:
#         prediction = pipe.predict(pd.DataFrame([input_data.dict()]))
#         prediction_int = int(prediction[0])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")
    
#     # Retourner la prédiction
#     return {"prediction": prediction_int}







@router.post("/predict/", dependencies=[Depends(has_access)])
async def predict(data: donnees_film):
    
    # Créer un dataframe à partir des données d'entrée
    input_df = pd.DataFrame([data.dict()])

    # Effectuer le prétraitement sur les données d'entrée avec le pipeline de prétraitement
    # try:
    # # Prétraitement des données d'entrée
    #     input_processed = pipe['preprocessor'].transform(input_df)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error during data preprocessing: {str(e)}")

    # Faire la prédiction avec le modèle CatBoost après prétraitement
   
    prediction = pipe.predict(input_df)  # Utiliser le modèle CatBoost
    prediction_int = int(prediction[0])  # Convertir la prédiction en entier si nécessaire
   
    experiment = mlflow.get_experiment_by_name("visualisation_predictions_cinéma")

# Si l'expérience n'existe pas, elle est créée
    if experiment is None:
            experiment_id = mlflow.create_experiment("visualisation_predictions_cinéma")
    else:
            experiment_id = experiment.experiment_id

    # Log des paramètres et de la prédiction dans MLflow
    with mlflow.start_run() as run:
         mlflow.log_params(data.dict())                   # Enregistre les paramètres d'entrée
         mlflow.log_metric("prediction", prediction_int)  # Enregistre la prédiction

    # Enregistrer la prédiction et les métriques dans SQLite
    try:
        with get_db_connection() as conn:
            conn.execute('''
            INSERT INTO predictions (country, genre, numero_semaine, duree, prediction)
            VALUES (?, ?, ?, ?, ?)
            ''', (data.country, data.genre, data.numero_semaine, data.durée, prediction_int))
            conn.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")
    

    # Incrémenter le compteur de prédictions
    # prediction_counter += 1

    # if prediction_counter % 3 == 0:  # Vérifie si le compteur est divisible par 3
    #     try:
    #         subprocess.Popen(["python", "drift.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Error running drift.py: {str(e)}")

    # Retourner la prédiction en tant que réponse de l'API
    return {"prediction": prediction_int}

#endpoint pour faciliter l'utilisateur à avoir accés au numéro de semaien concerné par la semaine de sortie sur laquelle est demandée la prédiction
@router.get("/images/numero_semaine.png")
async def get_image():
    image_path = os.path.join("images", "numero_semaine.png")
    return FileResponse(image_path)

# Endpoint pour afficher le formulaire d'entrée
# Endpoint pour afficher le formulaire d'entrée
@router.get("/test", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Formulaire de Prédiction</title>
        </head>
        <body>
            <h1>Faites une Prédiction</h1>
            <form action="/predict/" method="post">
                <label for="country">Pays:</label>
                <input type="text" name="country" required>
                
                <label for="genre">Genre:</label>
                <input type="text" name="genre" required>
                
                <label for="numero_semaine">Numéro de Semaine:</label>
                <input type="number" name="numero_semaine" required>
                
                <label for="durée">Durée:</label>
                <input type="number" name="durée" required>
                
                <button type="submit">Soumettre</button>
            </form>
            <h2>Aide:</h2>
            <img src="/images/numero_semaine.png" alt="Image d'aide" style="max-width: 400px;">
        </body>
    </html>
    """



