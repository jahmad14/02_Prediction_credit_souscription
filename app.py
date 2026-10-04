"""
Application Streamlit — Prédiction de souscription bancaire (Classification Doc 2 - Bank)
Modèle retenu : XGBoost Classifier avec StandardScaler et LabelEncoder
Lancement en local : streamlit run app.py
"""

import os
import joblib
import numpy as np
import streamlit as st

# ----------------------------------------------------------------------
# Configuration de la page
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Term Deposit Prediction",
    page_icon="🏦",
    layout="centered",
)

DESCRIPTION = (
    "Cette application permet de prédire si un client souscrira à un dépôt à terme bancaire (variable `y` : 'no' ou 'yes') "
    "à partir de ses informations socio-professionnelles, de l'historique des contacts et du contexte de campagne marketing."
)

# ----------------------------------------------------------------------
# Chargement des artefacts (mis en cache)
# ----------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    base_dir = os.path.dirname(__file__)
    model = joblib.load(os.path.join(base_dir, "best_model_clas.joblib"))
    encoders = joblib.load(os.path.join(base_dir, "encoders_clas.joblib"))
    scaler = joblib.load(os.path.join(base_dir, "scaler_clas.joblib"))
    return model, encoders, scaler


model, encoders, scaler = load_artifacts()

# Ordre exact des variables prédictrices dans le dataset d'entraînement
FEATURE_COLS = [
    "age", "job", "marital", "education", "housing", "loan", "contact",
    "month", "day_of_week", "duration", "campaign", "pdays", "previous", "poutcome"
]

# ----------------------------------------------------------------------
# Fonction de prédiction
# ----------------------------------------------------------------------
def predict_subscription(features_dict):
    encoded_values = []
    for col in FEATURE_COLS:
        val = features_dict[col]
        if col in encoders:
            val = encoders[col].transform([val])[0]
        encoded_values.append(val)
        
    raw_vector = np.array([encoded_values])
    scaled_vector = scaler.transform(raw_vector)
    
    pred_idx = model.predict(scaled_vector)[0]
    target_classes = encoders["y"].classes_
    predicted_class = target_classes[pred_idx]
    
    # Récupération des probabilités
    probas = None
    if hasattr(model, "predict_proba"):
        probas_raw = model.predict_proba(scaled_vector)[0]
        probas = {target_classes[i]: float(probas_raw[i]) for i in range(len(target_classes))}
        
    return predicted_class, probas


# ----------------------------------------------------------------------
# Interface utilisateur
# ----------------------------------------------------------------------
st.title("🏦 Bank Term Deposit Prediction")
st.write(DESCRIPTION)

with st.form("form_bank_prediction"):
    st.subheader("Informations du client et de la campagne")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Âge du client", min_value=18, max_value=100, value=35, step=1)
        job = st.selectbox("Profession (Job)", options=list(encoders["job"].classes_))
        marital = st.selectbox("État civil (Marital)", options=list(encoders["marital"].classes_))
        education = st.selectbox("Niveau d'études (Education)", options=list(encoders["education"].classes_))
        housing = st.selectbox("Prêt immobilier (Housing loan)", options=list(encoders["housing"].classes_))
        loan = st.selectbox("Prêt personnel (Personal loan)", options=list(encoders["loan"].classes_))
        contact = st.selectbox("Moyen de communication (Contact)", options=list(encoders["contact"].classes_))

    with col2:
        month = st.selectbox("Dernier mois de contact (Month)", options=list(encoders["month"].classes_))
        day_of_week = st.selectbox("Jour de la semaine (Day of week)", options=list(encoders["day_of_week"].classes_))
        duration = st.number_input("Durée du dernier contact (secondes)", min_value=0, max_value=5000, value=250, step=10)
        campaign = st.number_input("Nombre de contacts durant la campagne", min_value=1, max_value=50, value=1, step=1)
        pdays = st.number_input("Jours écoulés depuis contact précédent (999 si jamais)", min_value=0, max_value=999, value=999, step=1)
        previous = st.number_input("Nombre de contacts avant cette campagne", min_value=0, max_value=10, value=0, step=1)
        poutcome = st.selectbox("Résultat de la campagne précédente (Poutcome)", options=list(encoders["poutcome"].classes_))

    submit_btn = st.form_submit_button("Prédire la souscription", type="primary")

if submit_btn:
    try:
        inputs = {
            "age": age, "job": job, "marital": marital, "education": education,
            "housing": housing, "loan": loan, "contact": contact, "month": month,
            "day_of_week": day_of_week, "duration": duration, "campaign": campaign,
            "pdays": pdays, "previous": previous, "poutcome": poutcome
        }
        classe_predite, probas = predict_subscription(inputs)
        
        if classe_predite == "yes":
            st.success("✅ **Souscription prédite : OUI (Le client souscrira au dépôt à terme)**")
        else:
            st.warning("❌ **Souscription prédite : NON (Le client ne souscrira pas)**")
            
        if probas:
            st.write("### Probabilités estimées par le modèle XGBoost :")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric(label="Probabilité 'Non' (Refus)", value=f"{probas['no'] * 100:.1f} %")
            with col_p2:
                st.metric(label="Probabilité 'Oui' (Souscription)", value=f"{probas['yes'] * 100:.1f} %")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
