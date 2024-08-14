# Utiliser l'image de base officielle de Python 3.10.12
FROM python:3.10.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . .

# Exposer le port que l'application va utiliser
EXPOSE 8000

# Définir la commande par défaut pour lancer l'application
CMD ["uvicorn", "master1:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]




# Utiliser une image de base Python
# FROM python:3.10.12-slim

# # Définir le répertoire de travail dans le conteneur
# WORKDIR /app

# # Copier le fichier requirements.txt depuis la racine dans le répertoire de travail
# COPY requirements.txt ./

# # Installer les dépendances
# RUN pip install --no-cache-dir -r requirements.txt

# # Copier tout le code source du sous-dossier api_rest dans le répertoire de travail
# COPY api_rest /app/api_rest

# # Exposer le port que l'application va utiliser
# EXPOSE 8000

# # Définir la commande par défaut pour lancer l'application
# CMD ["uvicorn", "api_rest.master1:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

