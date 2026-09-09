# Refined experiment script fixing previous errors
import json
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

def run_experiment():
    print("Executing repaired experiment script...")
    X, y = make_regression(n_samples=1000, n_features=10, noise=15.0, random_state=42)
    X[:, 0] = np.exp(np.clip(X[:, 0] / 3.0, -2, 3))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler_base = StandardScaler()
    X_train_base = scaler_base.fit_transform(X_train)
    X_test_base = scaler_base.transform(X_test)
    model_base = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=100, random_state=42)
    model_base.fit(X_train_base, y_train)
    y_pred_base = model_base.predict(X_test_base)
    mse_base = mean_squared_error(y_test, y_pred_base)
    r2_base = r2_score(y_test, y_pred_base)

    scaler_var = QuantileTransformer(output_distribution='normal', random_state=42)
    X_train_var = scaler_var.fit_transform(X_train)
    X_test_var = scaler_var.transform(X_test)
    model_var = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=100, random_state=42)
    model_var.fit(X_train_var, y_train)
    y_pred_var = model_var.predict(X_test_var)
    mse_var = mean_squared_error(y_test, y_pred_var)
    r2_var = r2_score(y_test, y_pred_var)

    results = {
        "baseline_mse": float(round(mse_base, 4)),
        "baseline_r2": float(round(r2_base, 4)),
        "variant_mse": float(round(mse_var, 4)),
        "variant_r2": float(round(r2_var, 4)),
        "mse_improvement_pct": float(round((mse_base - mse_var) / mse_base * 100, 2))
    }
    print("EXPERIMENT_METRICS_JSON:" + json.dumps(results))
    return results

if __name__ == "__main__":
    run_experiment()