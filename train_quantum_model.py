                val_r2 = r2_score(y_test, val_preds.numpy())
            print(f"  Epoch [{epoch:2d}/{epochs:2d}] | Train MSE: {epoch_loss:.4f} | Val MSE: {val_mse:.4f} | Val MAE: {val_mae:.4f} eV | Val R2: {val_r2:.4f}")
    # 6. Evaluation
    print("\n[4/5] Evaluating Trained Quantum Model on Test Partition...")
    model.eval()
    with torch.no_grad():
        test_preds, test_expvals = model(X_test_t)
        test_preds_np = test_preds.numpy()
        mse = mean_squared_error(y_test, test_preds_np)
        mae = mean_absolute_error(y_test, test_preds_np)
        r2 = r2_score(y_test, test_preds_np)
    print(f"  Final Test Metrics:")
    print(f"    - Mean Squared Error (MSE) : {mse:.4f} eV^2")
    print(f"    - Mean Absolute Error (MAE): {mae:.4f} eV")
    print(f"    - R-Squared Score (R2)     : {r2:.4f}")
    # 7. Model Serialization
    print("\n[5/5] Exporting Trained Quantum Weights and Artifacts...")
    weights_np = model.q_weights.detach().cpu().numpy()
    readout_w = model.readout.weight.detach().cpu().item()
    readout_b = model.readout.bias.detach().cpu().item()
    artifact = {
        "model_type": "PennyLane_VQC_Hybrid",
        "n_qubits": N_QUBITS,
        "n_layers": N_LAYERS,
        "quantum_weights": weights_np,
        "readout_weight": readout_w,
        "readout_bias": readout_b,
        "feature_scaler": scaler,
        "feature_names": feature_cols,
        "sabatier_optimal_be": -1.05,
        "sabatier_sigma": 0.32,
        "metrics": {"test_mse": mse, "test_mae": mae, "test_r2": r2}
    }
    output_model_path = "quantum_catalyst_model.pkl"
    joblib.dump(artifact, output_model_path)
    print(f"Successfully saved quantum catalyst model artifact to '{output_model_path}'!")
    print("=" * 70)
    return artifact
if __name__ == "__main__":
    train_model()
