import unittest
from fastapi import status
from fastapi.testclient import TestClient
from main import app

class TestPredictEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # Test sans token d'authentification
    def test_predict_without_token(self):
        response = self.client.post("/predict/", json={"feature1": 0.5, "feature2": 1.5})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

if __name__ == "__main__":
    unittest.main()