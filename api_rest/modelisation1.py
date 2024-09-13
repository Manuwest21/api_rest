from fastapi import APIRouter, Depends
from pydantic import BaseModel
import pickle
import pandas as pd
import joblib
from utils2 import has_access
import mlflow
from typing import Dict, Any
import sqlite3
from sklearn.metrics import mean_squared_error, r2_score
from fastapi import HTTPException
from typing import Dict, Any
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
###111#
# Charger le modèle pickle
with open('modele_4_ml.pkl', 'rb') as f:
    model = pickle.load(f)

# Créer un routeur pour les endpoints de modelisation1
router = APIRouter()
def get_db_connection():
    try:
        conn = sqlite3.connect('predictions.db')
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")



mlflow.set_experiment("visualisation_predictions_cinéma")
# Définir une route pour effectuer des prédictions
@router.post("/predict/", dependencies=[Depends(has_access)])
async def predict(data: InputData):
    # Créer un dataframe à partir des données d'entrée
    input_df = pd.DataFrame([data.dict()])

    # Effectuer le prétraitement sur les données d'entrée
    # input_processed = pipe['preprocessor'].transform(input_df)

    # # Faire la prédiction avec le modèle
    #  prediction = pipe['log_reg'].predict(input_processed)
    prediction = model.predict(input_df)
    with mlflow.start_run() as run:
        mlflow.log_params(data.dict())  # Enregistrer les paramètres d'entrée
        mlflow.log_metric("prediction", prediction[0])  # Enregistrer la prédiction
    
    
    # Enregistrer la prédiction et les métriques dans SQLite
    conn = get_db_connection()
    conn.execute('''
    INSERT INTO predictions (country, genre, numero_semaine, duree, prediction)
    VALUES (?, ?, ?, ?, ?)
    ''', (data.country, data.genre, data.numero_semaine, data.durée, round(prediction[0])))
    conn.commit()
    conn.close()
    # Retourner la prédiction
    return {"prediction": prediction[0]}

# Exporter le routeur
