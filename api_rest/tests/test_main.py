import os
from datetime import datetime, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt
import sys
import os

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
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_token_generation_incorrect_credentials():
    response = client.post("/token", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}

# def test_predict_with_token():
#     token = get_token("admin")
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.post("/predict/", headers=headers, json={"feature1": 0.5, "feature2": 1.5})
#     assert response.status_code == status.HTTP_200_OK
#     assert "prediction" in response.json()

def test_predict_without_token():
    response = client.post("/predict/", json={"feature1": 0.5, "feature2": 1.5})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
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
    assert response.status_code == 422  # Unprocessable Entity
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