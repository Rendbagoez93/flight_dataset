import pandas as pd

def load_flight_data(file_path='data/flight_data_2024.csv'):
    df = pd.read_csv(file_path)
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
    # Create a copy to avoid modifying the original
    df_filled = df.copy()
    
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
    
# Descriptive Analysis
def analyze_flights_by_time(df):
    flights_per_dow = df.groupby('day_of_week').size()
    flights_per_month = df.groupby('month').size()
    
    print("\nFlights per Day of Week:")
    print(flights_per_dow)
    print("\nFlights per Month:")
    print(flights_per_month)
    
    return {
        'flights_per_dow': flights_per_dow,
        'flights_per_month': flights_per_month
    }

def analyze_flights_by_airport(df):
    flights_per_airport = df['origin'].value_counts()
    print("\nFlights per Airport:")
    print(flights_per_airport)
    
    return flights_per_airport

def analyze_cancellations(df):
    cancel_rate = df['cancelled'].mean() * 100
    cancel_by_month = df[df['cancelled'] == 1].groupby('month').size()
    cancel_by_origin = df[df['cancelled'] == 1].groupby('origin').size()
    
    print(f"\nCancellation Rate: {cancel_rate:.2f}%")
    print("\nCancellations by Month:")
    print(cancel_by_month)
    print("\nCancellations by Origin:")
    print(cancel_by_origin)
    
    return {
        'cancel_rate': cancel_rate,
        'cancel_by_month': cancel_by_month,
        'cancel_by_origin': cancel_by_origin
    }

def analyze_flight_duration_distance(df):
    duration_cols = ['air_time', 'taxi_out', 'taxi_in', 'distance']
    summary_stats = df[duration_cols].describe().round(2)
    
    print("\nFlight Duration & Distance Distribution:")
    print(summary_stats)
    
    return summary_stats

def analyze_delays(df):
    delay_cols = ['weather_delay', 'late_aircraft_delay']
    delay_summary = df[delay_cols].describe().round(2)
    total_delay = df[delay_cols].sum()
    
    print("\nDelay Descriptive Statistics:")
    print(delay_summary)
    print("\nTotal Delays:")
    print(total_delay)
    
    return {
        'delay_summary': delay_summary,
        'total_delay': total_delay
    }

def analyze_airport_performance(df):
    airport_summary = df.groupby('origin').agg({
        'air_time': 'mean',
        'taxi_out': 'mean',
        'weather_delay': 'mean',
        'late_aircraft_delay': 'mean'
    }).round(2).sort_values('weather_delay', ascending=False)
    
    print("\nAirport Performance Summary:")
    print(airport_summary)
    
    return airport_summary

def analyze_monthly_delays(df):
    monthly_delay = df.groupby('month')[['weather_delay', 'late_aircraft_delay']].mean().round(2)
    
    print("\nMonthly Delay Analysis:")
    print(monthly_delay)
    
    return monthly_delay

def perform_complete_analysis(df):
    results = {}
    
    results['time_analysis'] = analyze_flights_by_time(df)
    results['airport_analysis'] = analyze_flights_by_airport(df)
    results['cancellation_analysis'] = analyze_cancellations(df)
    results['duration_analysis'] = analyze_flight_duration_distance(df)
    results['delay_analysis'] = analyze_delays(df)
    results['airport_performance'] = analyze_airport_performance(df)
    results['monthly_delays'] = analyze_monthly_delays(df)
    
    return results

# Main execution (only runs when script is executed directly)
if __name__ == "__main__":
    # Run the complete preprocessing pipeline
    file_path = 'data/flight_data_2024.csv'
    processed_df = preprocess_flight_data(file_path)
    
    print("\nPreprocessing completed successfully!")
    print(f"Final dataset shape: {processed_df.shape}")
    
    # Perform descriptive analysis
    print("\n" + "="*50)
    print("DESCRIPTIVE ANALYSIS")
    print("="*50)
    
    analysis_results = perform_complete_analysis(processed_df)
    
    print("\nAnalysis completed successfully!")