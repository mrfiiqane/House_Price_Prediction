import json
import pandas as pd
import joblib
from Utilities import prepare_features_from_raw
import joblib
import urllib.request
import os

MODEL_URL = "https://github.com/mrfiiqane/House_Price_Prediction/raw/main/modeles/rf_model.joblib"
MODEL_PATH = "/tmp/rf_model.joblib"

if not os.path.exists(MODEL_PATH):
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

rf_model = joblib.load(MODEL_PATH)


# Load models once
MODELS = {
    "lr": joblib.load("modeles/lr_model.joblib"),
    "rf": joblib.load("modeles/rf_model.joblib")
}

def handler(request):
    try:
        body = request.get_json()
        choice = body.get("model", "lr").lower()
        if choice not in MODELS:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Unknown model. Use lr or rf"})
            }
        model = MODELS[choice]
        x_new = prepare_features_from_raw(body)
        pred = float(model.predict(x_new)[0])
        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": round(pred,2)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
