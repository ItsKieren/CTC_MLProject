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
from queue import Queue
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def convert_port(port):
    """Convert port numbers to hexadecimal format"""
    try:
        port = int(port)
        if port == 0 or pd.isna(port):
            return '0'
        return f'0x{port:04x}'
    except (ValueError, TypeError):
        return '0'

def convert_protocol(proto):
    """Convert protocol names to standard format"""
    proto = str(proto).lower()
    if proto in ['tcp', 'udp', 'icmp']:
        return proto
    return 'man'  # Default for unknown protocols

def convert_state(state):
    """Convert state values to standard format"""
    state = str(state).upper()
    if state in ['CON', 'RST', 'FIN', 'INT', 'REQ', 'RSP', 'ECO', 'CLO', 'ACC', 'TST', 'TXD', 'URP', 'URN', 'MAS', 'PAR']:
        return state
    return 'CON'  # Default for unknown states

def convert_data(data):
    """Convert the input data to match the training data format"""
    try:
        # Create a copy to avoid modifying the original
        df = data.copy()
        
        # Print original columns for debugging
        print("Original columns:", df.columns.tolist())
        
        # Convert column names to match training data
        column_mapping = {
            'Dst Port': 'Dport',
            'Src Port': 'Sport',
            'Protocol': 'Proto',
            'State Flags': 'State',
            'Duration (s)': 'Dur',
            'Out Bytes': 'SrcBytes',
            'In Bytes': 'DstBytes',
            'Total Packets': 'TotPkts',
            'Total Bytes': 'TotBytes'
        }
        
        # Rename columns that exist in the input data
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Print columns after mapping for debugging
        print("Columns after mapping:", df.columns.tolist())
        
        # Convert ports
        if 'Sport' in df.columns:
            df['Sport'] = df['Sport'].apply(convert_port)
        if 'Dport' in df.columns:
            df['Dport'] = df['Dport'].apply(convert_port)
        
        # Convert protocol
        if 'Proto' in df.columns:
            df['Proto'] = df['Proto'].apply(convert_protocol)
        
        # Convert state
        if 'State' in df.columns:
            df['State'] = df['State'].apply(convert_state)
        
        # Add missing columns with default values
        required_columns = ['SrcBytes', 'TotBytes', 'TotPkts', 'dTos', 'sTos']
        for col in required_columns:
            if col not in df.columns:
                if col in ['dTos', 'sTos']:
                    df[col] = 0  # Default TOS values
                else:
                    df[col] = 0  # Default for other missing columns
        
        # Define the exact order of columns as used in training
        training_columns = ['Dur', 'Proto', 'Sport', 'Dport', 'State', 'sTos', 'dTos', 'TotPkts', 'TotBytes', 'SrcBytes']
        
        # Reorder columns to match training order
        df = df[training_columns]
        
        # Fill missing values with 0
        df = df.fillna(0)
        
        # Print final columns for debugging
        print("Final columns:", df.columns.tolist())
        
        return df
    except Exception as e:
        print(f"Error during data conversion: {str(e)}")
        print("Available columns:", df.columns.tolist())
        raise

class CSVHandler(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue
        self.processed_files = set()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.csv'):
            if event.src_path not in self.processed_files:
                self.processed_files.add(event.src_path)
                self.queue.put(event.src_path)
                print(f"\n📥 Added to queue: {os.path.basename(event.src_path)}")

def load_model_and_encoders(model_path='models/random_forest_model.joblib', 
                          encoders_path='models/label_encoders.joblib'):
    """Load the trained model and label encoders"""
    if not os.path.exists(model_path) or not os.path.exists(encoders_path):
        raise FileNotFoundError("Model or encoders not found. Please train the model first.")
    
    model = joblib.load(model_path)
    label_encoders = joblib.load(encoders_path)
    return model, label_encoders

def preprocess_data(data, label_encoders):
    """Preprocess input data similar to training phase"""
    try:
        # Convert data format
        data = convert_data(data)
        
        # Handle categorical data
        categorical_cols = ['Proto', 'State', 'Sport', 'Dport']
        for col in categorical_cols:
            if col in data.columns:
                # Convert to string type first
                data[col] = data[col].astype(str)
                # Transform unknown values to most common training value
                unknown_mask = ~data[col].isin(label_encoders[col].classes_)
                if unknown_mask.any():
                    most_common = label_encoders[col].classes_[0]  # Use first value as default
                    data.loc[unknown_mask, col] = most_common
                data[col] = label_encoders[col].transform(data[col])
        
        return data
        
    except Exception as e:
        print(f"\n❌ Error in preprocessing: {str(e)}")
        print("Available columns:", data.columns.tolist())
        raise

def process_file(file_path, model, label_encoders, processed_dir, start_time):
    try:
        print(f"\n==================================================")
        print(f"📊 Processing Network Traffic File")
        print(f"==================================================")
        
        # Calculate time elapsed since start
        elapsed_time = time.time() - start_time
        print(f"⏱️ Time elapsed since start: {elapsed_time:.2f} seconds")
        
        print(f"\n📁 File: {os.path.basename(file_path)}")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        
        # Define output file path before any processing
        file_number = file_path.split('network_traffic-')[-1].split('.')[0]
        output_file = os.path.join(processed_dir, f'processed_network_traffic-{file_number}.csv')
        
        # Load and preprocess the data
        data = pd.read_csv(file_path)
        print(f"📈 Total flows analyzed: {len(data)}")
        
        # Preprocess the data
        processed_data = preprocess_data(data, label_encoders)
        
        # Make predictions
        predictions = model.predict(processed_data)
        prediction_counts = pd.Series(predictions).map({0: 'Benign', 1: 'Malicious'}).value_counts()
        
        print(f"\n==================================================")
        print(f"🔍 Analysis Results")
        print(f"==================================================")
        print(f"\nTraffic Classification:")
        for label, count in prediction_counts.items():
            print(f"  • {label}: {count} flows")
        
        # Add checkmarks for benign traffic
        if len(prediction_counts) == 1 and prediction_counts.index[0] == 'Benign':
            print("✓" * 50)
            print("✅ All traffic appears to be benign")
            print("✓" * 50)
        else:
            print("\n⚠️  ALERT: Potentially malicious traffic detected!")
            print("!" * 50)
        
        # Add predictions to the original data
        data['Prediction'] = predictions
        data.to_csv(output_file, index=False)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        
        # Calculate processing time
        processing_time = time.time() - start_time
        print(f"\n⏱️ Total processing time: {processing_time:.2f} seconds")
        
    except PermissionError:
        print(f"\n⚠️  File is currently locked or in use: {os.path.basename(file_path)}")
        print("⏳ Waiting 2 seconds before retrying...")
        time.sleep(2)
        try:
            # Retry the entire process
            data = pd.read_csv(file_path)
            print(f"📈 Total flows analyzed: {len(data)}")
            processed_data = preprocess_data(data, label_encoders)
            predictions = model.predict(processed_data)
            data['Prediction'] = predictions
            data.to_csv(output_file, index=False)
            print(f"\n✅ Successfully processed file after retry")
        except Exception as retry_error:
            print(f"\n❌ Error during retry: {str(retry_error)}")
    except Exception as e:
        print(f"\n❌ Error processing file: {str(e)}")
        print(f"File: {os.path.basename(file_path)}")

def process_queue(queue, model, label_encoders, processed_dir, start_time):
    while True:
        file_path = queue.get()
        if file_path is None:  # Poison pill to stop the worker
            break
        process_file(file_path, model, label_encoders, processed_dir, start_time)
        queue.task_done()

def monitor_directory(directory):
    print("\n==================================================")
    print("🚀 Network Traffic Monitor")
    print("==================================================")
    print(f"\n📂 Monitoring directory: {os.path.abspath(directory)}")
    print("⏳ Waiting for new network traffic files...")
    print("💡 Press Ctrl+C to stop monitoring")
    print("\n==================================================")
    
    # Create processed directory if it doesn't exist
    processed_dir = 'scapy_processed_files'
    Path(processed_dir).mkdir(exist_ok=True)
    
    print("\n==================================================")
    print("📚 Loading Analysis Model")
    print("==================================================")
    
    # Load the model and encoders
    model = joblib.load('models/random_forest_model.joblib')
    label_encoders = joblib.load('models/label_encoders.joblib')
    print("✅ Model loaded successfully!")
    
    print("\n==================================================")
    print("🎯 Monitor Active")
    print("==================================================")
    print(f"\n👀 Watching for new files in: {directory}")
    
    # Create a queue for file processing
    file_queue = Queue()
    
    # Create and start the file processor thread
    start_time = time.time()
    processor_thread = threading.Thread(
        target=process_queue,
        args=(file_queue, model, label_encoders, processed_dir, start_time),
        daemon=True
    )
    processor_thread.start()
    
    # Set up the file system observer
    event_handler = CSVHandler(file_queue)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n==================================================")
        print("🛑 Monitor Stopped")
        print("==================================================")
        observer.stop()
        # Add poison pill to stop the processor thread
        file_queue.put(None)
        processor_thread.join()
        print("\n👋 Thank you for using the Network Traffic Monitor!")
    
    observer.join()

if __name__ == "__main__":
    monitor_directory('scapy_packet_files') 
