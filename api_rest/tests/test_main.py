import os
from datetime import datetime, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt
import sys
import os
from modelisation import InputData

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from master1 import app

client = TestClient(app)

# def get_token(username: str):
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     ALGORITHM = "HS256"
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode = {"sub": username, "exp": datetime.utcnow() + access_token_expires}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

def test_token_generation():
    response = client.post("/token", data={"username": "admin", "password": "password123"})
    # assert response.status_code == status.200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_token_generation_incorrect_credentials():
    response = client.post("/token", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 404     #status.HTTP_401_UNAUTHORIZED 
    assert response.json() == {"detail": "Incorrect username or password"}

# def test_predict_with_token():
#     token = get_token("admin")
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.post("/predict/", headers=headers, json={"feature1": 0.5, "feature2": 1.5})
#     assert response.status_code == status.HTTP_200_OK
#     assert "prediction" in response.json()

def test_predict_without_token():
    response = client.post("/predict/", json={"Hfeature1": 0.5, "feature2": 1.5})
    assert response.status_code == status.HTTP_403_FORBIDDEN   #status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

client = TestClient(app)

def test_predict_with_invalid_data_types():
    # Test avec un float au lieu d'un int pour numero_semaine
    response = client.post("/predict/", json={
        "country": "France",
        "genre": "Drama",
        "public": "Tous publics",
        "distributeur": "Distributeur A",
        "numero_semaine": 0.5,  # Mauvais format
        "durée": 120,
        "directeur": "Directeur A",
        "acteur1": "Acteur A",
        "acteur2": "Acteur B",
        "acteur3": "Acteur C"
    })
    assert response..status_code == 403  # Unprocessable Entity  status_code == 422
    assert "value is not a valid integer" in response.json()["detail"][0]["msg"]

    # Test avec une chaîne au lieu d'un int pour durée
    response = client.post("/predict/", json={
        "country": "France",
        "genre": "Drama",
        "public": "Tous publics",
        "distributeur": "Distributeur A",
        "numero_semaine": 1,
        "durée": "long",  # Mauvais format
        "directeur": "Directeur A",
        "acteur1": "Acteur A",
        "acteur2": "Acteur B",
        "acteur3": "Acteur C"
    })
    assert response.status_code == 422  # Unprocessable Entity
    assert "value is not a valid integer" in response.json()["detail"][0]["msg"]


import pytest
from pydantic import ValidationError

def test_input_data_invalid_entries():
    # Données valides pour la référence
    valid_data = {
        "country": "France",
        "genre": "Comédie",
        "public": "Tous publics",
        "distributeur": "StudioCanal",
        "numero_semaine": 36,
        "durée": 90,
        "directeur": "Hervé Mimran",
        "acteur1": "Didier Bourdon",
        "acteur2": "Gérard Darmon",
        "acteur3": "Chantal Lauby"
    }
    
    # Test avec un champ vide pour country
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "country": ""})
    assert "Length must be between 1 and 15 characters" in str(excinfo.value)

    # Test avec un numéro de semaine invalide (0)
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "numero_semaine": 0})
    assert "numero_semaine must be between 1 and 52" in str(excinfo.value)

    # Test avec un numéro de semaine invalide (53)
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "numero_semaine": 53})
    assert "numero_semaine must be between 1 and 52" in str(excinfo.value)

    # Test avec une durée invalide (moins de 60 minutes)
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "durée": 45})
    assert "durée must be between 60 and 300 minutes" in str(excinfo.value)

    # Test avec une durée invalide (plus de 300 minutes)
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "durée": 301})
    assert "durée must be between 60 and 300 minutes" in str(excinfo.value)

    # Test avec une chaîne trop longue pour distributeur
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "distributeur": "A" * 16})
    assert "Length must be between 1 and 15 characters" in str(excinfo.value)

    # Test avec un champ vide pour genre
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "genre": ""})
    assert "Length must be between 1 and 15 characters" in str(excinfo.value)

    # Test avec un champ vide pour public
    with pytest.raises(ValidationError) as excinfo:
        InputData(**{**valid_data, "public": ""})
    assert "Length must be between 1 and 15 characters" in str(excinfo.value)
