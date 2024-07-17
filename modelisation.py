from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import pandas as pd
from preprocessing import preprocessing
import mlflow
import pickle 
import sqlite3

def load_training_data(df):
    # Charger les données d'entraînement depuis la base de données ou un fichier CSV
    # Assurez-vous d'ajuster ces lignes en fonction de votre cas d'utilisation
    # Exemple : charger les données à partir d'un fichier CSV
    # df = pd.read_csv('training_data.csv')
    train_df = df[df['date'] < 2019]
    test_df = df[df['date'] >= 2019]
    train_df.drop(['date'],axis=1)
    test_df.drop(['date'],axis=1)
# Diviser les ensembles en caractéristiques (X) et cible (y)
    X_train = train_df.drop('nbre_entrees', axis=1)  # Remplacez 'cible' par le nom de la colonne de votre cible
    y_train = train_df['nbre_entrees']
    # Diviser les données en features (X) et target (y)
    # X_train = df.drop('nbre_entrees', axis=1)  # Remplacez 'cible' par le nom de la colonne de votre cible
    # y_train = df['nbre_entrees']

    return X_train, y_train

def train_model(X_train, y_train):
    # Définir les caractéristiques ordinales et numériques
    ordinal_features = ['country', 'genre', 'public', 'distributeur', 'numero_semaine']
    numerical_features = ['durée', 'directeur', 'acteur1', 'acteur2', 'acteur3']

    # Définir les encodeurs pour les caractéristiques ordinales et numériques
    categorical_transformer = OneHotEncoder(sparse_output=True, handle_unknown='ignore')
    numerical_transformer = MinMaxScaler()

    # Créer le préprocesseur de colonnes
    preprocessor = ColumnTransformer(
        transformers=[
            ('other_cat', categorical_transformer, ordinal_features),
            ('num', numerical_transformer, numerical_features)
        ],
        remainder='drop'
    )

    # Créer le modèle CatBoostRegressor
    log_reg = CatBoostRegressor()

    # Créer le pipeline
    pipe = Pipeline([
         ('preprocessor', preprocessor),
         ('log_reg', log_reg)
    ])

    # Entraîner le pipeline
    pipe.fit(X_train, y_train)

    return pipe

def modelisation(connection, run_name):
    # Charger les données
    df = pd.read_csv('new_nettoyage.csv')  # Charger les données à partir du fichier CSV
    df = preprocessing(df)

    # Charger les données d'entraînement
    X_train, y_train = load_training_data(df)

    # Prétraiter les données d'entraînement

    # Entraîner le modèle
    trained_model = train_model(X_train, y_train)
    
    # Évaluer le modèlesss
    # Ces étapes peuvent être ajoutées ici si nécessaire
    with open('modele_5_ml.pkl', 'wb') as f:
        pickle.dump(trained_model, f)
    # Configurer MLflow
        
    y_pred = trained_model.predict(X_train)
    mae = mean_absolute_error(y_train, y_pred)
    mse = mean_squared_error(y_train, y_pred)
    r2 = r2_score(y_train, y_pred)
    
    # Enregistrer les métriques avec MLflow
    with mlflow.start_run() as run:
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)
    
    modele=12
    # Intégrer les métriques dans votre base de données SQLite3
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO metrics (nom_modele,mae, mse, r2) VALUES (?, ?, ?,?)", (modele,mae, mse, r2))
        connection.commit()
        cursor.close()
    # print type(trained_model)

    # Enregistrer le modèle dans MLflow
    mlflow.sklearn.log_model(trained_model, "trained_model1")

        
#     mlflow.set_tracking_uri('http://localhost:5000')
#     mlflow.set_experiment(run_name)

    
#     with mlflow.start_run() as run:
     
#         mlflow.log_param("run_name", run_name)

#         mlflow.sklearn.log_model(trained_model, "trained_model")

#     return run.info.run_id

if __name__ == "__main__":
    connection = sqlite3.connect("bdd.db")  # Connection à votre base de données
    run_id = modelisation(connection, "run_name")





# if __name__ == "__main__":
#     df = pd.read_csv('new_nettoyage.csv')  # Charger les données à partir du fichier CSV
#     df= preprocessing(df)
#     X_train, y_train = load_training_data(df)  # Charger les données d'entraînement

#     # Prétraiter les données d'entraînement
   

#     # Entraîner le modèle
#     trained_model = train_model(X_train, y_train)



# if __name__ == "__main__":
#     # Charger les données d'entraînement depuis la base de données ou un fichier CSV
#     # Assurez-vous de remplacer ces lignes par le chargement de vos données
#     X_train, y_train = load_training_data(df)

#     # Prétraiter les données d'entraînement
#     X_train_processed = preprocessing(X_train)

#     # Entraîner le modèle
#     trained_model = train_model(X_train_processed, y_train)
