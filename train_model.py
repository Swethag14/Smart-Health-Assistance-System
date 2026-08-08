import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
# Load datasets
train = pd.read_csv("Training.csv")
test = pd.read_csv("Testing.csv")
# Remove extra column if present
if "Unnamed: 133" in train.columns:
    train = train.drop("Unnamed: 133", axis=1)
if "Unnamed: 133" in test.columns:
    test = test.drop("Unnamed: 133", axis=1)
# Split features and target
X_train = train.drop("prognosis", axis=1)
y_train = train["prognosis"]
X_test = test.drop("prognosis", axis=1)
y_test = test["prognosis"]
# Encode disease labels
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
y_test = encoder.transform(y_test)
# ---------------- Random Forest ----------------
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
# ---------------- Decision Tree ----------------
dt = DecisionTreeClassifier(
    random_state=42
)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_pred)
# ---------------- Results ----------------
print("Random Forest Accuracy :", round(rf_accuracy * 100, 2), "%")
print("Decision Tree Accuracy :", round(dt_accuracy * 100, 2), "%")
# Save the best model
if rf_accuracy >= dt_accuracy:
    print("\nBest Model : Random Forest")
    joblib.dump(rf, "model.pkl")
else:
    print("\nBest Model : Decision Tree")
    joblib.dump(dt, "model.pkl")
joblib.dump(encoder, "label_encoder.pkl")
print("\nModel saved successfully.")