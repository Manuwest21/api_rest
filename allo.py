from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# Créer une classe pour les données d'entrée
class InputData(BaseModel):
    country: str
    genre: str
    public: str
    distributeur: str
    numero_semaine: int
    durée: int
    directeur: int
    acteur1: int
    acteur2: int
    acteur3: int

# Charger le modèle pickle
with open('modele_1_ml.pkl', 'rb') as f:
    model = pickle.load(f)

# Créer une instance de l'application FastAPI
app = FastAPI()

# Définir une route pour effectuer des prédictions
@app.post("/predict/")
async def predict(data: InputData):
    # Créer un dataframe à partir des données d'entrée
    input_df = pd.DataFrame([data.dict()])

    # Faire la prédiction avec le modèle
    prediction = model.predict(input_df)

    # Retourner la prédiction
    return {"prediction": prediction[0]}