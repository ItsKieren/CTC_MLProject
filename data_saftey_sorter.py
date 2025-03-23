import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import logging
import os
from pathlib import Path
import argparse

# Set up logging to document timestamps, errors, and messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_model_and_encoders(model_path='models/random_forest_model.joblib', 
                          encoders_path='models/label_encoders.joblib'):
    """Load the trained model and label encoders"""
    if not os.path.exists(model_path) or not os.path.exists(encoders_path):
        raise FileNotFoundError("Model or encoders not found. Please train the model first.")
    
    model = joblib.load(model_path)
    label_encoders = joblib.load(encoders_path)
    return model, label_encoders

def preprocess_data(data, label_encoders):
    """Preprocess the input data similar to training"""
    # Remove leading/trailing spaces from column names
    data.columns = data.columns.str.strip()
    
    # Drop the index column if it exists
    if 'Unnamed: 0' in data.columns:
        data = data.drop(columns=['Unnamed: 0'])
    
    # Drop non-numerical columns that aren't useful for prediction
    columns_to_drop = ['StartTime', 'SrcAddr', 'DstAddr', 'Dir', 'Label']
    data = data.drop(columns=[col for col in columns_to_drop if col in data.columns])
    
    # Handle missing values
    data = data.fillna(0)
    
    # Handle categorical data
    categorical_cols = ['Proto', 'State', 'Sport', 'Dport']
    for col in categorical_cols:
        if col in data.columns:
            # Convert to string type first
            data[col] = data[col].astype(str)
            # Use the same encoder from training
            data[col] = label_encoders[col].transform(data[col])
    
    return data

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Make predictions using the trained model')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('--output', '-o', default='predictions.csv',
                      help='Path to save the predictions (default: predictions.csv)')
    args = parser.parse_args()

    try:
        # Load the model and encoders
        logging.info("Loading model and encoders...")
        model, label_encoders = load_model_and_encoders()
        
        # Load the data to predict
        if not os.path.exists(args.input_file):
            raise FileNotFoundError(f"Input file '{args.input_file}' not found")
        
        logging.info(f"Loading data from {args.input_file}...")
        data = pd.read_csv(args.input_file)
        
        # Preprocess the data
        X = preprocess_data(data, label_encoders)
        
        # Make predictions
        logging.info("Making predictions...")
        predictions = model.predict(X)
        
        # Convert numeric predictions back to original labels
        original_labels = label_encoders['Label'].inverse_transform(predictions)
        
        # Add predictions to the original data
        data['Predicted_Label'] = original_labels
        
        # Save results
        data.to_csv(args.output, index=False)
        logging.info(f"Predictions saved to {args.output}")
        
        # Print prediction counts
        prediction_counts = pd.Series(original_labels).value_counts()
        print("\nPrediction Counts:")
        print(prediction_counts)
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
