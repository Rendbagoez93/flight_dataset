from data_preprocess import preprocess_flight_data


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

def display_basic_stats(df):
    """
    Display basic statistics about the flight dataset.
    
    Args:
        df (pd.DataFrame): Flight dataset
    
    Returns:
        dict: Dictionary containing basic statistics
    """
    stats = {
        'total_flights': len(df),
        'cancelled_flights': df['cancelled'].sum() if 'cancelled' in df.columns else 0,
        'average_distance': round(df['distance'].mean(), 2) if 'distance' in df.columns else 0
    }
    
    print(f"Total flights: {stats['total_flights']}")
    print(f"Cancelled flights: {stats['cancelled_flights']}")
    print(f"Average distance: {stats['average_distance']} miles")
    
    return stats

def perform_complete_analysis(df):
    """
    Perform complete descriptive analysis of flight dataset.
    
    Args:
        df (pd.DataFrame): Flight dataset
    
    Returns:
        dict: Dictionary containing all analysis results
    """
    results = {}
    
    # Display basic statistics first
    results['basic_stats'] = display_basic_stats(df)
    
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