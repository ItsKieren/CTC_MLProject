import pandas as pd
import numpy as np
import logging
import argparse
import joblib

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load training data to get unique values
try:
    training_data = pd.read_csv('raw_labelled_flow.csv')
    print("\nUnique Sport values in training data:", list(training_data['Sport'].unique())[:20])
    print("Unique Dport values in training data:", list(training_data['Dport'].unique())[:20])
except Exception as e:
    print(f"Error loading training data: {e}")

def convert_protocol(protocol):
    """Convert protocol numbers to their string representations"""
    protocol_map = {
        '1': 'icmp',
        '6': 'tcp',
        '17': 'udp',
        '2': 'igmp',
        '47': 'gre',
        '50': 'esp',
        '51': 'ah',
        '89': 'ospf',
        '132': 'sctp'
    }
    return protocol_map.get(str(protocol), 'man')  # Default to 'man' for unknown protocols

def convert_state(state):
    """Convert state flags to match training data format"""
    if pd.isna(state) or state == '':
        return 'CON'  # Default state for empty values
    
    # Map TCP states to training data states
    state_map = {
        'ACK': 'CON',
        'SYN': 'CON',
        'FIN': 'FIN',
        'RST': 'RST',
        'PSH': 'CON',
        'URG': 'CON'
    }
    
    # Check if any of the TCP flags are in the state
    for flag, mapped_state in state_map.items():
        if flag in str(state):
            return mapped_state
    
    return 'CON'  # Default state for any other values

def convert_port(port):
    """Convert port numbers to match training data format."""
    # Known port values from training data
    known_ports = {
        '0': '0',
        'nfs': 'nfs',
        '2050': '2050',
        '2051': '2051',
        '2048': '2048',
        '2052': '2052',
        'netbios-ns': 'netbios-ns',
        '1025': '1025',
        '1027': '1027',
        'netbios-dgm': 'netbios-dgm',
        '1035': '1035',
        '1039': '1039',
        '1040': '1040',
        '1041': '1041',
        '1042': '1042',
        '1044': '1044',
        '1045': '1045',
        '1046': '1046',
        '1047': '1047',
        '1049': '1049',
        'ftp': 'ftp',
        'domain': 'domain',
        'http': 'http',
        '1900': '1900',
        '65520': '65520',
        '2012': '2012',
        '888': '888',
        '82': '82',
        'netbios-ssn': 'netbios-ssn',
        '81': '81',
        'https': 'https',
        '3128': '3128',
        'ircd': 'ircd',
        'smtp': 'smtp',
        '65500': '65500',
        '9381': '9381',
        '8399': '8399'
    }
    
    # Handle zero and invalid values
    if pd.isna(port) or port == 0:
        return '0'
    
    try:
        port = int(port)
        if port < 0 or port > 65535:
            return '0'
    except (ValueError, TypeError):
        return '0'
    
    # Convert to string
    port_str = str(port)
    
    # If it's a known port, return it
    if port_str in known_ports:
        return port_str
    
    # For unknown ports, return '0'
    return '0'

def convert_data(input_file, output_file):
    """Convert network traffic data to match training data format"""
    try:
        # Read the input data
        logging.info(f"Reading data from {input_file}...")
        data = pd.read_csv(input_file)
        
        # Create a new DataFrame with the required columns
        converted_data = pd.DataFrame()
        
        # Map the columns
        column_mapping = {
            'StartTime': pd.Timestamp.now(),  # Using current time as placeholder
            'Dur': 'Duration (s)',
            'Proto': 'Protocol',
            'SrcAddr': 'Src IP',
            'Sport': 'Src Port',
            'Dir': 'Direction',
            'DstAddr': 'Dst IP',
            'Dport': 'Dst Port',
            'State': 'State Flags',
            'sTos': 0,  # Setting to 0 as it's not in the new data
            'dTos': 0,  # Setting to 0 as it's not in the new data
            'TotPkts': 'Total Packets',
            'TotBytes': 'Total Bytes',
            'SrcBytes': 'Out Bytes'
        }
        
        # Map the columns that exist
        for new_col, old_col in column_mapping.items():
            if old_col in data.columns:
                if new_col == 'Proto':
                    # Convert protocol numbers to strings
                    converted_data[new_col] = data[old_col].apply(convert_protocol)
                elif new_col == 'State':
                    # Convert state flags to match training data format
                    converted_data[new_col] = data[old_col].apply(convert_state)
                elif new_col in ['Sport', 'Dport']:
                    # Convert port numbers to hexadecimal format
                    converted_data[new_col] = data[old_col].apply(convert_port)
                else:
                    converted_data[new_col] = data[old_col]
            else:
                converted_data[new_col] = 0  # Fill missing columns with 0
        
        # Add missing columns that were in the training data
        missing_columns = ['Label']  # Add any other missing columns here
        for col in missing_columns:
            converted_data[col] = 0  # Fill with 0 or appropriate default value
        
        # Handle missing values
        converted_data = converted_data.fillna(0)
        
        # Convert categorical columns to strings
        categorical_cols = ['Proto', 'State', 'Sport', 'Dport']
        for col in categorical_cols:
            if col in converted_data.columns:
                converted_data[col] = converted_data[col].astype(str)
        
        # Save the converted data
        converted_data.to_csv(output_file, index=False)
        logging.info(f"Converted data saved to {output_file}")
        
        # Print sample of converted data
        print("\nSample of converted data:")
        print(converted_data.head())
        
        # Print column information
        print("\nColumns in converted data:")
        print(converted_data.columns.tolist())
        
        # Print unique values in categorical columns
        print("\nUnique values in categorical columns:")
        for col in categorical_cols:
            if col in converted_data.columns:
                print(f"{col}: {list(converted_data[col].unique())[:10]}")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert network traffic data to match training data format')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('--output', '-o', default='converted_data.csv',
                      help='Path to save the converted data (default: converted_data.csv)')
    args = parser.parse_args()
    
    convert_data(args.input_file, args.output)

if __name__ == "__main__":
    main() 
