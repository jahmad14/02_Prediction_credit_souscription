# Déploiement : Prédiction de Souscription Bancaire (Classification Doc 2 - Bank)

Cette application Streamlit permet de prédire si un client bancaire souscrira à un produit d'épargne (dépôt à terme, variable cible `y` : `no` ou `yes`) en exploitant ses données socio-démographiques, son historique de contact et les variables de campagne marketing.

## Modèle retenu et artefacts
- **Modèle final :** `XGBClassifier` (`best_model_clas.joblib`), sélectionné pour son meilleur score F1 (0.870) et son excellente régularisation sur le jeu de validation.
- **Normalisation :** `StandardScaler` (`scaler_clas.joblib`).
- **Encodeurs catégoriels :** Dictionnaire de `LabelEncoder` (`encoders_clas.joblib`) pour `job`, `marital`, `education`, `housing`, `loan`, `contact`, `month`, `day_of_week`, `poutcome` et la cible `y`.

## Lancement en local
```bash
cd "Rendu/Supervised/Classification/Doc 2/Deployment"
streamlit run app.py
```
