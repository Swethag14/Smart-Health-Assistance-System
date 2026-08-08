import joblib
import pandas as pd

model = joblib.load("model.pkl")
encoder = joblib.load("label_encoder.pkl")

# Load feature names
df = pd.read_csv("Training.csv")

if "Unnamed: 133" in df.columns:
    df = df.drop("Unnamed: 133", axis=1)

features = list(df.drop("prognosis", axis=1).columns)


def predict_disease(selected_symptoms):

    patient = {feature: 0 for feature in features}

    for symptom in selected_symptoms:
        if symptom in patient:
            patient[symptom] = 1

    patient = pd.DataFrame([patient])

    prediction = model.predict(patient)

    disease = encoder.inverse_transform(prediction)

    return disease[0]