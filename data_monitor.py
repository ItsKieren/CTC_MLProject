import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import logging
import os
from pathlib import Path
import time
from datetime import datetime
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CSVHandler(FileSystemEventHandler):
    def __init__(self, model, label_encoders):
        self.model = model
        self.label_encoders = label_encoders
        self.processed_files = set()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.csv'):
            print(f"\nNew file detected: {event.src_path}")
            process_new_file(event.src_path, self.model, self.label_encoders)
            self.processed_files.add(event.src_path)

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

def process_new_file(file_path, model, label_encoders):
    """Process a new CSV file and make predictions"""
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)
        
        # Preprocess the data
        X = preprocess_data(data, label_encoders)
        
        # Make predictions
        predictions = model.predict(X)
        
        # Convert numeric predictions back to original labels
        original_labels = label_encoders['Label'].inverse_transform(predictions)
        
        # Count predictions
        prediction_counts = pd.Series(original_labels).value_counts()
        
        # Print results
        print(f"\n=== Predictions for {file_path} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        print("Prediction Counts:")
        print(prediction_counts)
        
        # Check for malicious traffic
        malicious_count = prediction_counts.get('Zero_access', 0) + prediction_counts.get('Neris', 0)
        if malicious_count > 0:
            print(f"\n⚠️ ALERT: {malicious_count} potentially malicious flows detected!")
        else:
            print("\n✅ All traffic appears to be benign.")
        
        # Add predictions to the original data
        data['Predicted_Label'] = original_labels
        
        # Save results with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'predictions_{timestamp}.csv'
        data.to_csv(output_file, index=False)
        print(f"\nDetailed predictions saved to {output_file}")
        
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")

def monitor_directory(directory='scapy_packet_files'):
    """Monitor a directory for new CSV files and process them immediately"""
    print(f"Starting monitoring in directory: {os.path.abspath(directory)}")
    print("Waiting for new CSV files...")
    print("Press Ctrl+C to stop monitoring")
    
    # Create directory if it doesn't exist
    Path(directory).mkdir(exist_ok=True)
    
    # Load model and encoders once
    print("\nLoading model and encoders...")
    model, label_encoders = load_model_and_encoders()
    print("Model and encoders loaded successfully!")
    
    # Set up the event handler and observer
    event_handler = CSVHandler(model, label_encoders)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    
    try:
        # Start the observer
        observer.start()
        print(f"\nMonitoring started. Waiting for new files in {directory}...")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        print("\n\nMonitoring stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise
    finally:
        observer.join()

if __name__ == "__main__":
    # Monitor the scapy_packet_files directory
    DIRECTORY = 'scapy_packet_files'
    monitor_directory(DIRECTORY) 
