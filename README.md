Projet API de prédiction des entrées en salle de cinéma
1. Contexte du Projet

Les gérants de salle de cinéma rencontrent des difficultés à déterminer le nombre de salles à allouer pour chaque nouveau film. Ils s'appuient souvent sur leur propre estimation de l’affluence que le film pourrait avoir lors de sa première semaine de sortie en France, une tâche qui peut s'avérer longue et peu fiable. Pour les aider, nous mettons en place une API sécurisée intégrant un modèle de machine learning capable de fournir des prédictions robustes sur l'affluence des films.

Pour garantir la pérennité et la qualité de cette API, nous avons prévu la mise en place d'une chaîne d'intégration continue (CI) et de livraison continue (CD). Ce processus automatisé intégrera les phases de tests nécessaires pour valider chaque aspect de l’API, facilitant ainsi sa maintenance, des mises à jour régulières, et un fonctionnement optimal. L'intégration du modèle au sein d'une API REST permettra à d'autres applications ou services d'utiliser facilement ces prédictions via des requêtes API. Ce modèle prend en entrée plusieurs caractéristiques du film (ex. : genre, durée, budget, popularité des acteurs, etc.) et produit une prédiction.
2. Mise en Place d’une API

Une API REST sécurisée a été créée pour exposer les fonctionnalités d'un modèle d'intelligence artificielle utilisant CatBoost, qui repose sur des arbres de décision pour effectuer des prédictions. Cette API est principalement structurée autour de deux points de terminaison :

    /token : Permet l'authentification des utilisateurs via un mécanisme sécurisé.
    /predict : Offre la possibilité de soumettre des caractéristiques de films à l'affiche et de recevoir des prédictions sur le nombre d'entrées en salle que le film réalisera lors de sa première semaine de sortie en France.

L'authentification est requise pour accéder à ces endpoints, garantissant ainsi un accès restreint et sécurisé aux services de l'API. Par ailleurs, l'API inclut un point de terminaison /docs, qui fournit une documentation interactive détaillant l’ensemble des endpoints disponibles et leur utilisation.
3. Méthodologie Générale

Le développement de l'API s'inscrit dans une démarche MLOps (Machine Learning Operations), qui combine des pratiques de développement logiciel (DevOps) avec le déploiement et la gestion de modèles d'intelligence artificielle. Ce processus garantit une intégration continue (CI) et une livraison continue (CD), permettant des mises à jour rapides, un contrôle de qualité strict, et une collaboration efficace entre les équipes de développement et de data science. Nous utilisons GitHub Actions pour automatiser les tests, les validations et les déploiements, structurant ainsi ce flux de travail.
4. Principaux Outils et Technologies Utilisés

Les outils et technologies principaux employés dans ce projet incluent :

    Python : Utilisé pour le développement de l'API et l'implémentation du modèle de machine learning.
    CatBoost : Modèle d'IA optimisé pour les données catégorielles, utilisé pour prédire les entrées en salles de cinéma.
    FastAPI : Framework pour créer l'API REST, offrant des performances élevées et une gestion intégrée de la documentation.
    OAuth2 et JWT : Pour gérer l'authentification et sécuriser l'accès à l'API.
    MLflow : Pour le suivi des prédictions et des versions de modèles.
    Streamlit : Pour le tableau de bord interactif de visualisation des prédictions et la surveillance du drift.
    Seaborn : Pour la génération de visualisations, telles que les boxplots et swarmplots, permettant de surveiller d'éventuels drifts dans les données via une analyse visuelle des distributions.
    GitHub : Pour le versionnage du code source du projet : GitHub Repo
    GitHub Actions : Pour automatiser les pipelines CI/CD (Continuous Integration, Continuous Deployment), assurant ainsi une livraison continue fluide, en exécutant et vérifiant automatiquement la réussite des tests, afin de garantir la qualité et la fiabilité du code à chaque mise à jour.

5. Conclusion

Ce projet fournira aux gérants de salle de cinéma un outil puissant et efficace pour prévoir l'affluence des films, leur permettant ainsi de mieux gérer l'allocation des salles et d'optimiser leurs ressources. Grâce à une API sécurisée et des prédictions basées sur des données précises, nous espérons améliorer leur prise de décision et accroître leur efficacité opérationnelle.
