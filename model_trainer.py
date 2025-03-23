import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import logging
import os
from pathlib import Path

# Set up logging to document timestamps, errors, and messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # Check if training dataset exists in the current directory
        if not os.path.exists('./raw_labelled_flow.csv'):
            raise FileNotFoundError("Dataset file 'raw_labelled_flow.csv' not found in current directory")

        # Load the dataset
        logging.info("Loading dataset...")
        data = pd.read_csv('./raw_labelled_flow.csv')
        
        # Remove leading/trailing spaces from column names
        data.columns = data.columns.str.strip()
        
        # Drop the index column if it exists
        if 'Unnamed: 0' in data.columns:
            data = data.drop(columns=['Unnamed: 0'])
        
        # Print dataset information
        logging.info(f"Dataset shape: {data.shape}")
        logging.info(f"Columns in the dataset: {data.columns.tolist()}")
        
        # Convert ports to strings for printing
        data['Sport'] = data['Sport'].astype(str)
        data['Dport'] = data['Dport'].astype(str)
        
        # Print unique values before encoding
        print("\nUnique values in training data:")
        print("States:", data['State'].unique())
        print("Protocols:", data['Proto'].unique())
        print("Source Ports:", sorted(data['Sport'].unique())[:10], "...")
        print("Destination Ports:", sorted(data['Dport'].unique())[:10], "...")
        
        # Drop non-numerical columns that are less important for training, and difficult to train
        columns_to_drop = ['StartTime', 'SrcAddr', 'DstAddr', 'Dir']
        data = data.drop(columns=[col for col in columns_to_drop if col in data.columns])
        
        # Handle missing values in our dataset by filling missing values with 0
        data = data.fillna(0)
        
        # Initialize dictionary to store label converted ports and other columns
        label_encoders = {}
        
        # Handle categorical data similar to ports
        categorical_cols = ['Proto', 'State', 'Sport', 'Dport']
        for col in categorical_cols:
            if col in data.columns:
                # Convert to string type first
                data[col] = data[col].astype(str)
                label_encoders[col] = LabelEncoder()
                data[col] = label_encoders[col].fit_transform(data[col])
                logging.info(f"Encoded {col} with {len(label_encoders[col].classes_)} unique values")
        
        # Separate features and target
        X = data.drop(columns=['Label'])
        y = data['Label']
        
        # Encode target labels
        label_encoders['Label'] = LabelEncoder()
        y = label_encoders['Label'].fit_transform(y)
        logging.info(f"Encoded labels with {len(label_encoders['Label'].classes_)} unique values")
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logging.info(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
        
        # Initialize and train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        logging.info("Training model...")
        model.fit(X_train, y_train)
        
        # Check for overfitting by comparing train and test accuracy
        train_pred = model.predict(X_train)
        train_accuracy = accuracy_score(y_train, train_pred)
        
        test_pred = model.predict(X_test)
        test_accuracy = accuracy_score(y_test, test_pred)
        
        # Print training overview with focus on overfitting
        logging.info("\n=== Overfitting Check ===")
        logging.info(f"Training Accuracy: {train_accuracy:.4f}")
        logging.info(f"Test Accuracy: {test_accuracy:.4f}")
        logging.info(f"Difference: {(train_accuracy - test_accuracy):.4f}")
        
        if train_accuracy - test_accuracy > 0.05:
            logging.warning("Model might be overfitting (difference > 5%)")
        else:
            logging.info("No significant overfitting detected")
            
        report = classification_report(y_test, test_pred)
        print("\nClassification Report:")
        print(report)
        
        # Print feature importance for prioratization
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10))
        
        # Save the model and encoders for identification in the future
        output_dir = 'models'
        Path(output_dir).mkdir(exist_ok=True)
        joblib.dump(model, f'{output_dir}/random_forest_model.joblib')
        joblib.dump(label_encoders, f'{output_dir}/label_encoders.joblib')
        
        logging.info(f"Model and encoders saved to {output_dir}/")
        logging.info("Training completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
