from pathlib import Path
import pandas as pd
import numpy as np
import os
import joblib
ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT_DIR / "models"

BOROUGH_MAP = {
    'Manhattan': 1,
    'Bronx': 2,
    'Brooklyn': 3,
    'Queens': 4,
    'Staten Island': 5
}

BOROUGH_MAE = {
    1: 1600000, 
    2: 125000,       
    3: 450000,       
    4: 150000,       
    5: 110000       
}

def predict_sale_price(data: dict):
    borough = data.get("borough")
    borough_id = BOROUGH_MAP.get(borough)
    try:
        model, encoder = get_model_encoder(borough=borough_id)
        
        input_df = pd.DataFrame({
            'GROSS SQUARE FEET': [float(data.get("gross_sqft"))],
            'LAND SQUARE FEET': [float(data.get("land_sqft"))],
            'YEAR BUILT': [int(data.get("year_built"))],
            'ZIP CODE': [int(data.get("zip_code"))],
            'BUILDING CLASS CATEGORY': [data.get("prop_type")]
        })
        input_df.loc[:, 'BUILDING CLASS CATEGORY'] = input_df.loc[:, 'BUILDING CLASS CATEGORY'].astype(str)
        input_df['BUILDING CLASS CATEGORY'] = encoder.transform(input_df[['BUILDING CLASS CATEGORY']])
        
        log_pred = model.predict(input_df)[0]
        pred = np.expm1(log_pred)
        
        margin_error = BOROUGH_MAE.get(borough_id)
        min_price = max(0, pred - margin_error)
        max_price = pred + margin_error
        return {
            "estimated_price": float(pred),
            "margin_error": float(margin_error),
            "range_low": float(min_price),
            "range_high": float(max_price)
        }
    except ValueError as e:
        return str(e)
    

def get_model_encoder(borough: int):
    model_path = os.path.join(MODEL_DIR, "models", f"model_borough_{borough}.joblib")
    encoder_path = os.path.join(MODEL_DIR, "encoders", f"encoder_borough_{borough}.joblib")
    if not os.path.exists(model_path) or not os.path.exists(encoder_path):
        raise ValueError(f"Model or encoder not found for borough {borough}")
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    return model, encoder