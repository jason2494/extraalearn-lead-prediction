# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from pathlib import Path
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
learn_api = Flask("ExtraaLearn")

# Load the trained lead conversion model
model = joblib.load(Path(__file__).with_name("learn_model.joblib"))

# The 13 features the model expects, in order
FEATURES = [
    'age', 'current_occupation', 'first_interaction', 'profile_completed',
    'website_visits', 'time_spent_on_website', 'page_views_per_visit',
    'last_activity', 'print_media_type1', 'print_media_type2',
    'digital_media', 'educational_channels', 'referral'
]

# Define a route for the home page
@learn_api.get('/')
def home():
    return "Welcome to the Lead Prediction System"

# Define an endpoint to predict conversion for a single lead
@learn_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Send a JSON object containing the lead features.'}), 400
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({'error': f"Missing columns: {', '.join(missing)}"}), 400
    # Build a one-row DataFrame with the features in order
    input_data = pd.DataFrame([{f: data[f] for f in FEATURES}])
    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]
    # Return the prediction as a JSON response
    return jsonify({'Lead': prediction})

# Define an endpoint to predict conversion for a batch of leads from a CSV
@learn_api.post('/v1/predict_batch')
def predict_batch():
    # Get the uploaded CSV file from the request
    file = request.files.get('file')
    if file is None:
        return jsonify({'error': 'No CSV file uploaded. Attach it as form field "file".'}), 400
    try:
        df = pd.read_csv(file)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
        return jsonify({'error': 'Upload a valid, nonempty UTF-8 CSV.'}), 400
    if df.empty or df.isna().any().any():
        return jsonify({'error': 'CSV must contain lead rows without missing values.'}), 400
    # Check that every required column is present
    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        return jsonify({'error': f"Missing columns: {', '.join(missing)}"}), 400
    # Predict for every row, using only the columns the model expects
    df = df.drop(columns=['ID', 'status'], errors='ignore')
    df['prediction'] = model.predict(df.loc[:, FEATURES]).tolist()
    # Return all rows with their predictions
    return jsonify({'predictions': df.to_dict(orient='records')})

# Run the Flask app in debug mode (gunicorn is used in the Dockerfile)
if __name__ == '__main__':
    learn_api.run(debug=True)
