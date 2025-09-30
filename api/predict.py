from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Utilities import prepare_features_from_raw

app = Flask(__name__)
CORS(app)

MODELS = {
    "lr": joblib.load("modeles/lr_model.joblib"),
    "rf": joblib.load("modeles/rf_model.joblib")
}

@app.route("/predict", methods=["POST"])
def predict():
    choice = request.args.get("model", "").lower()
    if choice not in MODELS:
        return jsonify({"error": "Unknown model. Use model=lr or model=rf"}), 400
    model = MODELS[choice]

    data = request.get_json(silent=True) or {}
    required = ["Size_sqft", "Bedrooms", "Bathrooms", "YearBuilt", "Location"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        x_new = prepare_features_from_raw(data)
        pred = float(model.predict(x_new)[0])
    except Exception as e:
        return jsonify({"error": f"Failed to prepare/predict: {e}"}), 500

    return jsonify({
        "model": "linear_regression" if choice=="lr" else "random_forest",
        "input": data,
        "prediction": round(pred, 2)
    })
