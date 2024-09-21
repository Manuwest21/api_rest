import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import pickle
import pandas as pd
import joblib
from securite import has_access
import mlflow
from typing import Dict, Any
import sqlite3

# Charger le pipeline depuis le fichier
pipe = joblib.load('pipeline_model.joblib')

# Créer une classe pour les données d'entrée
class InputData(BaseModel):
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

# Charger le modèle pickle
with open('modele_4_ml.pkl', 'rb') as f:
    model = pickle.load(f)

# Créer un routeur pour les endpoints de modelisation1
router = APIRouter()

# Chemin vers le fichier CSV
csv_file = 'predictions.csv'

# Définir une fonction pour vérifier si le fichier CSV existe
def append_to_csv(data: dict, prediction: float):
    # Ajouter la prédiction aux données d'entrée
    data['prediction'] = round(prediction, 2)
    
    # Convertir les données en dataframe pandas
    df = pd.DataFrame([data])
    
    # Vérifier si le fichier existe, append si oui, sinon créer un nouveau fichier
    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, index=False, mode='w', header=True)  # Écrire avec l'entête
    else:
        df.to_csv(csv_file, index=False, mode='a', header=False)  # Append sans entête

mlflow.set_experiment("visualisation_predictions_cinéma")

# Définir une route pour effectuer des prédictions
@router.post("/predict/", dependencies=[Depends(has_access)])
async def predict(data: InputData):
    # Créer un dataframe à partir des données d'entrée
    input_df = pd.DataFrame([data.dict()])

    # Effectuer le prétraitement sur les données d'entrée
    input_processed = pipe['preprocessor'].transform(input_df)

    # Faire la prédiction avec le modèle
    prediction = pipe['log_reg'].predict(input_processed)

    with mlflow.start_run() as run:
        mlflow.log_params(data.dict())  # Enregistrer les paramètres d'entrée
        mlflow.log_metric("prediction", prediction[0])  # Enregistrer la prédiction
    
    # Enregistrer la prédiction dans le fichier CSV
    append_to_csv(data.dict(), prediction[0])

    # Retourner la prédiction
    return {"prediction": round(prediction[0], 2)}