import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib

def run_training():
    print("[1/4] Preparing dataset for the complete catalyst catalog...")

    # Features: [atomic_num, electronegativity, d_electrons, coordination_n, carbon_support_ratio]
    # Targets:  [energy_barrier, stability_index, selectivity, activity]
    catalog_catalysts = [
        {"features": [78.0, 2.28, 9.0, 0, 0.80], "targets": [8.5, 9.5, 0.98, 0.97]},   # Pt/C Benchmark
        {"features": [34.0, 1.95, 5.8, 6, 0.20], "targets": [9.2, 9.1, 0.97, 0.95]},   # FeMoco Native Mimic
        {"features": [44.0, 2.20, 7.0, 4, 0.00], "targets": [9.6, 9.2, 0.96, 0.94]},   # Ru1/TiO2
        {"features": [42.0, 2.16, 5.0, 3, 0.90], "targets": [10.2, 8.7, 0.95, 0.93]},  # Mo/graphene SAC
        {"features": [26.5, 1.85, 6.5, 4, 0.70], "targets": [10.8, 8.5, 0.95, 0.93]},  # Fe-Co-N-C
        {"features": [26.0, 1.83, 6.0, 4, 0.75], "targets": [11.2, 8.2, 0.96, 0.94]},  # Fe-N4-C
        {"features": [34.0, 1.99, 5.5, 4, 0.65], "targets": [12.4, 8.0, 0.94, 0.91]},  # Fe-Mo-N-C
        {"features": [73.0, 1.50, 3.0, 3, 0.50], "targets": [12.8, 8.4, 0.93, 0.90]},  # Ta/C3N4
        {"features": [24.5, 1.75, 4.5, 6, 0.20], "targets": [13.2, 8.6, 0.92, 0.89]},  # FeVco Bio-mimic
        {"features": [42.0, 2.16, 5.0, 2, 0.40], "targets": [13.5, 7.9, 0.91, 0.88]},  # MoS2-SV
        {"features": [23.0, 1.63, 3.0, 4, 0.70], "targets": [14.1, 7.5, 0.90, 0.89]},  # VN/N-C
        {"features": [23.0, 1.63, 3.0, 3, 0.80], "targets": [14.4, 7.3, 0.89, 0.87]},  # V-Nx/C
        {"features": [27.5, 1.86, 8.0, 4, 0.30], "targets": [14.8, 7.6, 0.88, 0.86]},  # CuFe Bimetallic
        {"features": [41.0, 1.60, 4.0, 4, 0.75], "targets": [15.1, 7.8, 0.89, 0.85]},  # Nb-N4 Single Atom
        {"features": [6.0,  2.55, 0.0, 3, 0.60], "targets": [15.6, 7.0, 0.87, 0.83]},  # g-C3N4-NV
        {"features": [83.0, 2.02, 0.0, 2, 0.00], "targets": [16.0, 6.8, 0.86, 0.81]},  # BiOBr-OV
        {"features": [42.0, 2.16, 5.0, 4, 0.40], "targets": [11.5, 8.8, 0.94, 0.92]},  # Schrock Catalyst
        {"features": [24.0, 1.65, 4.0, 4, 0.00], "targets": [16.5, 6.6, 0.85, 0.80]}   # Fe-TiO2 Defect
    ]

    np.random.seed(42)
    X_rows, y_rows = [], []

    for item in catalog_catalysts:
        feat, targ = item["features"], item["targets"]
        X_rows.append(feat)
        y_rows.append(targ)
        for _ in range(25):
            noise = np.random.normal(0, 0.02, 5)
            x_aug = [
                max(1.0, feat[0] + noise[0]),
                max(0.5, feat[1] + noise[1]),
                max(0.0, feat[2] + noise[2]),
                int(np.clip(round(feat[3] + noise[3]), 0, 8)),
                float(np.clip(feat[4] + noise[4], 0.0, 1.0))
            ]
            y_aug = [
                float(targ[0] + (noise[0] * 1.5)),
                float(np.clip(targ[1] + (noise[1] * 2.0), 1.0, 10.0)),
                float(np.clip(targ[2] + (noise[2] * 0.02), 0.50, 0.99)),
                float(np.clip(targ[3] + (noise[3] * 0.02), 0.50, 0.99))
            ]
            X_rows.append(x_aug)
            y_rows.append(y_aug)

    X, y = np.array(X_rows), np.array(y_rows)

    df = pd.DataFrame(np.hstack((X, y)), columns=[
        "atomic_num", "electronegativity", "d_electrons", "coordination_n", "carbon_support_ratio",
        "energy_barrier", "stability_index", "selectivity", "activity"
    ])
    df.to_csv("catalyst_training_data.csv", index=False)
    print(f"[2/4] Saved dataset with {len(df)} samples to 'catalyst_training_data.csv'.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[3/4] Training Multi-Output Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=150, max_depth=8, min_samples_split=3, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"      -> R² Score: {r2_score(y_test, preds, multioutput='uniform_average'):.4f}")
    print(f"      -> MSE: {mean_squared_error(y_test, preds):.4f}")

    joblib.dump(model, "catalyst_model.pkl")
    print("[4/4] Trained model successfully saved as 'catalyst_model.pkl'.")

if __name__ == "__main__":
    run_training()