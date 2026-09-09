import json
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import (
    MinMaxScaler,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)


def run_experiment():
    # Set seed for reproducibility
    np.random.seed(42)

    # Generate synthetic classification dataset
    X, y = make_classification(
        n_samples=2000,
        n_features=25,
        n_informative=15,
        n_redundant=5,
        n_clusters_per_class=2,
        flip_y=0.05,
        random_state=42,
    )

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Base configuration for MLP classifiers
    mlp_kwargs = {
        "hidden_layer_sizes": (64, 32),
        "activation": "relu",
        "solver": "adam",
        "max_iter": 300,
        "early_stopping": True,
        "n_iter_no_change": 10,
    }

    # ---------------------------------------------------------
    # BASELINE: Ensemble of 5 MLPs (varied seeds), all StandardScaler
    # ---------------------------------------------------------
    base_scaler = StandardScaler()
    X_train_base = base_scaler.fit_transform(X_train)
    X_test_base = base_scaler.transform(X_test)

    baseline_probs = []
    for i in range(5):
        clf = MLPClassifier(random_state=i, **mlp_kwargs)
        clf.fit(X_train_base, y_train)
        probs = clf.predict_proba(X_test_base)
        baseline_probs.append(probs)

    avg_baseline_probs = np.mean(baseline_probs, axis=0)
    baseline_preds = np.argmax(avg_baseline_probs, axis=1)
    baseline_acc = float(accuracy_score(y_test, baseline_preds))

    # ---------------------------------------------------------
    # VARIANT: Ensemble of 5 MLPs trained on 5 distinct Scalers
    # ---------------------------------------------------------
    scalers = [
        StandardScaler(),
        QuantileTransformer(output_distribution="normal", random_state=42),
        PowerTransformer(method="yeo-johnson"),
        RobustScaler(),
        MinMaxScaler(),
    ]

    variant_probs = []
    for i, scaler in enumerate(scalers):
        X_train_tr = scaler.fit_transform(X_train)
        X_test_tr = scaler.transform(X_test)

        clf = MLPClassifier(random_state=i, **mlp_kwargs)
        clf.fit(X_train_tr, y_train)
        probs = clf.predict_proba(X_test_tr)
        variant_probs.append(probs)

    avg_variant_probs = np.mean(variant_probs, axis=0)
    variant_preds = np.argmax(avg_variant_probs, axis=1)
    variant_acc = float(accuracy_score(y_test, variant_preds))

    results = {
        "baseline_test_accuracy": baseline_acc,
        "variant_test_accuracy": variant_acc,
    }

    print("EXPERIMENT_METRICS_JSON:" + json.dumps(results))


if __name__ == "__main__":
    run_experiment()