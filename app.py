from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

CATALYST_DESCRIPTORS = {
    # 1. Biological Benchmark (Native Nitrogenase Mimic)
    "femoco-native": {
        "name": "FeMoco Native Mimic",
        "formula": "MoFe₇S₉C-Coordinated Pincer",
        "features": [34.0, 1.95, 5.8, 6, 0.20]
    },
    # 2. Vanadium-Based Biomimic (Alternative Nitrogenase)
    "fevco-biomimic": {
        "name": "FeVco Bio-mimic",
        "formula": "VFe₇S₉C Vanadium-Nitrogenase Model",
        "features": [24.5, 1.75, 4.5, 6, 0.20]
    },
    # 3. High-Performance Single-Atom Catalyst (Molybdenum)
    "mo-graphene": {
        "name": "Mo/graphene SAC",
        "formula": "Single-Atom Molybdenum on Graphene",
        "features": [42.0, 2.16, 5.0, 3, 0.90]
    },
    # 4. High-Performance Single-Atom Catalyst (Iron-Nitrogen-Carbon)
    "fe-n4-c": {
        "name": "Fe-N₄-C",
        "formula": "Iron Tetra-Nitrogen Carbon",
        "features": [26.0, 1.83, 6.0, 4, 0.75]
    },
    # 5. Synergistic Dual Single-Atom Catalyst
    "fe-co-n-c": {
        "name": "Fe-Co-N-C",
        "formula": "Dual Single-Atom Carbon",
        "features": [26.5, 1.85, 6.5, 4, 0.70]
    },
    # 6. Metal-Free Defect Engineering (Nitrogen Vacancies)
    "g-c3n4-nv": {
        "name": "g-C₃N₄-NV",
        "formula": "Graphitic Carbon Nitride (N-Vacancies)",
        "features": [6.0, 2.55, 0.0, 3, 0.60]
    },
    # 7. Landmark Synthetic Molecular Complex
    "schrock-cat": {
        "name": "Schrock Catalyst",
        "formula": "[Mo(HIPTN₃N)] Coordination Complex",
        "features": [42.0, 2.16, 5.0, 4, 0.40]
    },
    # 8. Standard Baseline (Electrocatalysis Control)
    "pt-c": {
        "name": "Pt/C Benchmark",
        "formula": "20 wt% Platinum Carbon",
        "features": [78.0, 2.28, 9.0, 0, 0.80]
    }
}

MODEL_PATH = "catalyst_model.pkl"
ml_model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def predict_catalyst_properties(name, formula, features, candidate_id="custom"):
    feat_vector = np.array([features])
    
    if ml_model:
        pred = ml_model.predict(feat_vector)[0]
        energy_barrier = round(float(pred[0]), 1)
        stability_num = float(pred[1])
        selectivity = round(float(pred[2]), 2)
        activity = round(float(pred[3]), 2)
    else:
        energy_barrier, stability_num, selectivity, activity = 12.0, 7.5, 0.90, 0.88

    stability_label = "Very High" if stability_num >= 9.0 else "High" if stability_num >= 7.0 else "Moderate"
    score = round(float((selectivity * 0.4 + activity * 0.4 + (1 - energy_barrier / 30) * 0.2) * 100), 1)
    potential = "Top Candidate" if score >= 94 else "High Potential" if score >= 90 else "Viable Candidate"

    return {
        "id": candidate_id,
        "name": name,
        "formula": formula,
        "energy_barrier": energy_barrier,
        "stability": stability_label,
        "selectivity": selectivity,
        "activity": activity,
        "score": score,
        "potential": potential,
        "estimated_energy_reduction": int(round(score * 0.35)),
        "estimated_co2_reduction": int(round(score * 0.30))
    }

@app.route('/')
def dashboard():
    candidates = [
        predict_catalyst_properties(meta["name"], meta["formula"], meta["features"], cid)
        for cid, meta in CATALYST_DESCRIPTORS.items()
    ]
    sorted_catalysts = sorted(candidates, key=lambda x: x["score"], reverse=True)
    return render_template(
        'index.html',
        catalysts=sorted_catalysts,
        top=sorted_catalysts[0],
        total=len(sorted_catalysts)
    )

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True) or {}
    mode = data.get('mode', 'preset')

    if mode == 'custom':
        name = data.get('custom_name', 'Custom Catalyst')
        formula = data.get('custom_formula', 'User Defined Spec')
        try:
            features = [
                float(data.get('atomic_num', 26)),
                float(data.get('electronegativity', 1.8)),
                float(data.get('d_electrons', 6)),
                float(data.get('coordination_n', 4)),
                float(data.get('carbon_support_ratio', 0.7))
            ]
        except (ValueError, TypeError):
            features = [26, 1.8, 6, 4, 0.7]

        result = predict_catalyst_properties(name, formula, features, candidate_id="custom")
        return jsonify(result)

    candidate_id = data.get('candidate_id')
    meta = CATALYST_DESCRIPTORS.get(candidate_id)
    if not meta:
        return jsonify({"error": "Catalyst not found"}), 404

    result = predict_catalyst_properties(meta["name"], meta["formula"], meta["features"], candidate_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)