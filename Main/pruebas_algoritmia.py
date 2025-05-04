import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# --- Datos sintéticos simulando espectros ---
np.random.seed(42)
n_muestras = 100
longitudes_de_onda = np.linspace(200, 800, 600)  # 600 variables, de 200 nm a 800 nm
X = np.random.rand(n_muestras, len(longitudes_de_onda))

# Simulamos que la concentración depende fuertemente de unas pocas longitudes (ej. 300 y 500 nm)
concentracion = (
    3 * X[:, 100] + 5 * X[:, 300] + np.random.normal(0, 0.1, size=n_muestras)
)

# --- Dividir los datos ---
X_train, X_test, y_train, y_test = train_test_split(X, concentracion, test_size=0.2)

# --- Entrenar modelo ---
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Obtener importancia de variables ---
importancias = model.feature_importances_

# --- Graficar ---
plt.figure(figsize=(10, 4))
plt.plot(longitudes_de_onda, importancias)
plt.xlabel("Longitud de onda (nm)")
plt.ylabel("Importancia de la característica")
plt.title("Importancia de cada longitud de onda en la predicción")
plt.grid(True)
plt.tight_layout()
plt.show()
