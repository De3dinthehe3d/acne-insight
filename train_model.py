"""
train_model.py — Run once before launching app.py
"""

import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "acne_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

CATEGORICAL_COLS = ["skin_type", "acne_location", "diet_type", "exercise"]
TARGET_COL       = "acne_type"
FEATURE_COLS     = ["skin_type","acne_location","severity","sleep_hours",
                    "water_intake_liters","stress_level","diet_type","exercise","sweat_level"]

encoders   = {}
df_encoded = df.copy()

for col in CATEGORICAL_COLS:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    encoders[col] = le

target_encoder = LabelEncoder()
df_encoded[TARGET_COL] = target_encoder.fit_transform(df[TARGET_COL])
encoders[TARGET_COL] = target_encoder

X = df_encoded[FEATURE_COLS]
y = df_encoded[TARGET_COL]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=5,
                               class_weight="balanced", random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\nTest Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

importances = pd.Series(model.feature_importances_, index=FEATURE_COLS)
print("\nFeature Importances:")
print(importances.sort_values(ascending=False).to_string())

with open(os.path.join(MODEL_DIR, "acne_rf_model.pkl"),  "wb") as f: pickle.dump(model, f)
with open(os.path.join(MODEL_DIR, "label_encoders.pkl"), "wb") as f: pickle.dump(encoders, f)
with open(os.path.join(MODEL_DIR, "feature_cols.pkl"),   "wb") as f: pickle.dump(FEATURE_COLS, f)
print("\nModel saved to models/")
