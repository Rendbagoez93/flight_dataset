import pandas as pd
import os
import glob
from pathlib import Path

def load_flight_data(file_path='data/flight_data_2024.csv'):
    """
    Load flight dataset from CSV file with Kaggle environment auto-detection.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: Loaded and processed dataset
    """
    # Auto-detect data file (Kaggle mount or local)
    data_file = None
    if os.path.exists('/kaggle/input'):
        matches = glob.glob('/kaggle/input/**/flight_data_2024.csv', recursive=True)
        if matches:
            data_file = matches[0]
    if data_file is None:
        local_path = Path(file_path)
        if local_path.exists():
            data_file = str(local_path)
        else:
            # Fallback to original parameter
            data_file = file_path
    
    print(f'Using data file: {data_file}')
    df = pd.read_csv(data_file)
    
    # Enhanced data processing
    # Convert date column
    if 'fl_date' in df.columns:
        df['fl_date'] = pd.to_datetime(df['fl_date'], errors='coerce')
        
        # Ensure month column exists
        if 'month' not in df.columns:
            df['month'] = df['fl_date'].dt.month
        
        # Ensure day_of_week column exists
        if 'day_of_week' not in df.columns:
            df['day_of_week'] = df['fl_date'].dt.dayofweek + 1
    
    # Create readable day names
    dow_map = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
    df['day_name'] = df['day_of_week'].map(dow_map).fillna('Unknown')
    
    return df

def display_dataset_info(df):
    print("Dataset Information:")
    print(df.info())
    print("\nFirst 5 Rows of the Dataset:")
    print(df.head())
    print("\nStatistical Summary:")
    print(df.describe().round(2))

def check_missing_values(df):
    missing_values = df.isnull().sum()
    print("\nMissing Values in Each Column:")
    print(missing_values)
    return missing_values

def fill_missing_values(df):
    """
    Fill missing values with mean and median strategies with enhanced error handling.
    
    Args:
        df (pd.DataFrame): Dataset with missing values
    
    Returns:
        pd.DataFrame: Dataset with filled missing values
    """
    # Create a copy to avoid modifying the original
    df_filled = df.copy()
    
    # Drop rows missing essential data (only columns that exist)
    essential_cols = ['origin', 'dep_time', 'distance', 'air_time']
    existing_essentials = [c for c in essential_cols if c in df_filled.columns]
    if existing_essentials:
        df_filled = df_filled.dropna(subset=existing_essentials)
    
    # Fill NaN delay values with 0 (no delay) — defensive check
    for col in ['weather_delay', 'late_aircraft_delay']:
        if col in df_filled.columns:
            df_filled[col] = df_filled[col].fillna(0)
        else:
            df_filled[col] = 0
    
    # Fill missing values with appropriate strategies
    fill_values = {}
    
    # Fill with mean for these columns
    for col in ['dep_time', 'taxi_out', 'wheels_off', 'wheels_on', 'taxi_in']:
        if col in df_filled.columns:
            fill_values[col] = df_filled[col].mean()
    
    # Fill with median for these columns
    for col in ['air_time']:
        if col in df_filled.columns:
            fill_values[col] = df_filled[col].median()
    
    # Fill all at once
    df_filled = df_filled.fillna(value=fill_values)
    
    return df_filled

def verify_imputation(df):
    missing_after = df.isnull().sum()
    print("\nMissing Values After Imputation:")
    print(missing_after)
    return missing_after

def preprocess_flight_data(file_path='data/flight_data_2024.csv', verbose=True):
    # Load the dataset
    df = load_flight_data(file_path)
    
    if verbose:
        # Display basic information
        display_dataset_info(df)
        
        # Check for missing values
        check_missing_values(df)
    
    # Fill missing values
    df_processed = fill_missing_values(df)
    
    if verbose:
        # Verify imputation
        verify_imputation(df_processed)
    
    return df_processed

# Main execution (only runs when script is executed directly)
if __name__ == "__main__":
    # Run the complete preprocessing pipeline
    file_path = 'data/flight_data_2024.csv'
    processed_df = preprocess_flight_data(file_path)
    
    print("\nPreprocessing completed successfully!")
    print(f"Final dataset shape: {processed_df.shape}")