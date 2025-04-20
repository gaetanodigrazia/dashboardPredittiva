
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# Carica il dataset (assicurati che contenga SalePrice e feature pronte)
df = pd.read_csv("feature_engineered_train.csv")

# Separazione feature e target
X = df.drop(columns=["SalePrice"])
y = df["SalePrice"]

# Split dei dati
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inizializza e addestra il modello
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Valutazione
y_pred = model.predict(X_test)
print("R²:", round(r2_score(y_test, y_pred), 4))
print("RMSE:", round(mean_squared_error(y_test, y_pred, squared=False), 2))

# Salva il modello per l'uso nella dashboard
joblib.dump(model, "xgb_model.pkl")
print("✅ Modello salvato come xgb_model.pkl")
