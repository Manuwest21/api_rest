import pandas as pd
import numpy as np

def preprocessing(df):
    # Nettoyage des données
    df['date'] = df['date'].apply(lambda x: int(x[0:4]))  # Convertir la colonne 'date' en entier

    # Suppression des colonnes indésirables
    df = df.drop(['Unnamed: 0', 'titre', 'acteurs', 'box_office_france', 'prix', 'nominations', 'note_presse'], axis=1)

    # Création des dictionnaires pour directeur et acteurs
    sub_df = df[['directeur', 'acteur1', 'acteur2', 'acteur3', 'director_moy_entr', 'acteur1_moy_entr', 'acteur2_moy_entr', 'acteur3_moy_entr']]
    director_dict = {}
    actor_dict = {}

    for index, row in sub_df.iterrows():
        director_dict[row['directeur']] = row['director_moy_entr']
        actor_dict[row['acteur1']] = row['acteur1_moy_entr']
        actor_dict[row['acteur2']] = row['acteur2_moy_entr']
        actor_dict[row['acteur3']] = row['acteur3_moy_entr']

    # Calcul des quantiles pour les directeurs
    values = list(director_dict.values())
    quantiles = np.percentile(values, range(10, 101, 10))
    for i, quantile in enumerate(quantiles, start=1):
        print(f"Q{i}: {quantile}")

    # Calcul des quantiles pour les acteurs
    values = list(actor_dict.values())
    quantiles = np.percentile(values, range(10, 101, 10))
    for i, quantile in enumerate(quantiles, start=1):
        print(f"Q{i}: {quantile}")

    # Mapping des valeurs des dictionnaires sur le dataframe
    df['directeur'] = df['directeur'].map(director_dict)
    df['acteur1'] = df['acteur1'].map(actor_dict)
    df['acteur2'] = df['acteur2'].map(actor_dict)
    df['acteur3'] = df['acteur3'].map(actor_dict)

    # Renommage de la colonne 'budget_def' en 'budget' et suppression des caractères non numériques
    df.rename(columns={'budget_def':'budget'}, inplace=True)
    df['budget'] = df['budget'].str.replace('[\$ ]', '', regex=True)

    # Filtrage des valeurs dans certaines colonnes
    pays = ['Moins de 18 ans']
    mask = ~df['public'].isin(pays)
    df = df[mask]

    pays = ['Buddy-movie']
    mask = ~df['genre'].isin(pays)
    df = df[mask]

    pays = ['Liban', 'Islande', 'Afrique du Sud']
    mask = ~df['country'].isin(pays)
    df = df[mask]

    valeurs = ['Metro Goldwyn Mayer', 'Les Films 13', 'Night Ed Films', 'Paname Distribution', 'Alba Longa', 'Distrib Films', 'JML Productions', 'MC4 Distribution', 'Mica Films', 'Bellissima Films', 'Aramis Films', 'KMBO', 'Tadrart Films', 'Potemkine Films', 'Gémini Films', 'Steward', 'Surreal Films', 'Chrysalide', 'The Jokers / Les Bookmakers', 'Alfama Films', 'Stone Angels', 'Artedis']
    mask = ~df['distributeur'].isin(valeurs)
    df = df[mask]

    genre_counts = df['genre'].value_counts()
    mask = df['genre'].isin(genre_counts[genre_counts >= 3].index)
    df = df.loc[mask]

    genre_counts = df['country'].value_counts()
    mask = df['country'].isin(genre_counts[genre_counts >= 3].index)
    df = df.loc[mask]

    return df


if __name__ == "__main__":
    df = pd.read_csv('new_nettoyage.csv')
    processed_df = preprocessing(df)
