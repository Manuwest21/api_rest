from fastapi import APIRouter, Depends
from pydantic import BaseModel
import pickle
import pandas as pd
import joblib
from utils2 import has_access

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

# Définir une route pour effectuer des prédictions
@router.post("/predict/", dependencies=[Depends(has_access)])
async def predict(data: InputData):
    # Créer un dataframe à partir des données d'entrée
    input_df = pd.DataFrame([data.dict()])

    # Effectuer le prétraitement sur les données d'entrée
    input_processed = pipe['preprocessor'].transform(input_df)

    # Faire la prédiction avec le modèle
    prediction = pipe['log_reg'].predict(input_processed)

    # Retourner la prédiction
    return {"prediction": prediction[0]}

# Exporter le routeur
