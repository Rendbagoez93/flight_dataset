# Time Series Analysis - Seasonal Decomposition

import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
from data_preprocess import load_flight_data

warnings.filterwarnings("ignore")

def prepare_time_series_data(df):
    """
    Prepare time series data by aggregating flight metrics by date.
    
    Args:
        df (pd.DataFrame): Raw flight data
        
    Returns:
        pd.DataFrame: Daily aggregated time series data
    """
    # Create a copy and ensure fl_date is properly formatted
    ts_df = df.copy()
    
    # Aggregate data by date
    daily_flights = ts_df.groupby('fl_date').agg({
        'origin': 'count',  # Count of flights
        'cancelled': ['sum', 'mean'],  # Total and rate of cancellations
        'dep_time': 'count',  # Alternative flight count (non-null departures)
        'air_time': ['mean', 'std'],  # Average and variability of air time
        'distance': ['mean', 'sum'],  # Average and total distance
        'weather_delay': ['sum', 'mean'],  # Weather delay metrics
        'late_aircraft_delay': ['sum', 'mean'],  # Late aircraft delay metrics
        'taxi_out': 'mean',  # Average taxi out time
        'taxi_in': 'mean'   # Average taxi in time
    }).round(2)
    
    # Flatten column names
    daily_flights.columns = [
        'flight_count', 'cancellations_total', 'cancellation_rate',
        'departed_flights', 'avg_air_time', 'air_time_std',
        'avg_distance', 'total_distance', 'weather_delay_total',
        'avg_weather_delay', 'late_delay_total', 'avg_late_delay',
        'avg_taxi_out', 'avg_taxi_in'
    ]
    
    # Add derived metrics
    daily_flights['operational_efficiency'] = (
        daily_flights['avg_air_time'] / daily_flights['avg_distance'] * 1000
    ).round(3)  # minutes per 1000 miles
    
    daily_flights['delay_intensity'] = (
        daily_flights['weather_delay_total'] + daily_flights['late_delay_total']
    ) / daily_flights['flight_count']  # average total delay per flight
    
    # Add day of week and other temporal features
    daily_flights['day_of_week'] = daily_flights.index.dayofweek
    daily_flights['day_name'] = daily_flights.index.day_name()
    daily_flights['is_weekend'] = daily_flights['day_of_week'].isin([5, 6])
    
    return daily_flights

def seasonal_decomposition_analysis(ts_data, column, model='additive', period=7):
    """
    Perform seasonal decomposition on a time series.
    
    Args:
        ts_data (pd.DataFrame): Time series data with datetime index
        column (str): Column name to decompose
        model (str): 'additive' or 'multiplicative'
        period (int): Seasonal period (7 for weekly, 30 for monthly patterns)
        
    Returns:
        statsmodels.tsa.seasonal.DecomposeResult: Decomposition results
    """
    # Ensure we have enough data points
    if len(ts_data) < 2 * period:
        print(f"Warning: Need at least {2 * period} data points for period={period}")
        print(f"Current data length: {len(ts_data)}")
        period = min(period, len(ts_data) // 2)
        print(f"Adjusting period to: {period}")
    
    # Handle missing values
    series = ts_data[column].fillna(method='ffill').fillna(method='bfill')
    
    # Perform decomposition
    decomposition = seasonal_decompose(
        series, 
        model=model, 
        period=period,
        extrapolate_trend='freq'
    )
    
    return decomposition

def plot_seasonal_decomposition(decomposition, title="Seasonal Decomposition", figsize=(15, 12)):
    """
    Plot seasonal decomposition results.
    
    Args:
        decomposition: Results from seasonal_decompose
        title (str): Plot title
        figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(4, 1, figsize=figsize)
    
    # Original series
    decomposition.observed.plot(ax=axes[0], title=f'{title} - Original', color='blue')
    axes[0].set_ylabel('Original')
    axes[0].grid(True, alpha=0.3)
    
    # Trend
    decomposition.trend.plot(ax=axes[1], title='Trend Component', color='red')
    axes[1].set_ylabel('Trend')
    axes[1].grid(True, alpha=0.3)
    
    # Seasonal
    decomposition.seasonal.plot(ax=axes[2], title='Seasonal Component', color='green')
    axes[2].set_ylabel('Seasonal')
    axes[2].grid(True, alpha=0.3)
    
    # Residual
    decomposition.resid.plot(ax=axes[3], title='Residual Component', color='orange')
    axes[3].set_ylabel('Residual')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def analyze_seasonal_patterns(ts_data, metrics=['flight_count', 'cancellation_rate', 'avg_air_time']):
    """
    Analyze seasonal patterns for multiple metrics.
    
    Args:
        ts_data (pd.DataFrame): Time series data
        metrics (list): List of metrics to analyze
        
    Returns:
        dict: Dictionary containing decomposition results and insights
    """
    results = {}
    
    for metric in metrics:
        if metric in ts_data.columns:
            print(f"\n{'='*50}")
            print(f"Analyzing Seasonal Patterns: {metric}")
            print(f"{'='*50}")
            
            # Weekly patterns (period=7)
            try:
                weekly_decomp = seasonal_decomposition_analysis(ts_data, metric, period=7)
                results[f'{metric}_weekly'] = weekly_decomp
                
                # Calculate seasonal strength
                seasonal_strength = 1 - (weekly_decomp.resid.var() / 
                                       (weekly_decomp.seasonal + weekly_decomp.resid).var())
                
                print(f"Weekly Seasonal Strength: {seasonal_strength:.3f}")
                print(f"Trend Direction: {'Increasing' if weekly_decomp.trend.dropna().iloc[-1] > weekly_decomp.trend.dropna().iloc[0] else 'Decreasing'}")
                
                # Visualize
                plot_seasonal_decomposition(
                    weekly_decomp, 
                    title=f'{metric.replace("_", " ").title()} - Weekly Patterns'
                )
                plt.savefig(f'outputs/seasonal_decomp_{metric}_weekly.png', dpi=300, bbox_inches='tight')
                plt.show()
                
            except Exception as e:
                print(f"Error in weekly decomposition for {metric}: {e}")
        
        else:
            print(f"Warning: Column '{metric}' not found in data")
    
    return results

def day_of_week_analysis(ts_data):
    """
    Analyze day-of-week patterns in detail.
    
    Args:
        ts_data (pd.DataFrame): Time series data
        
    Returns:
        pd.DataFrame: Day of week statistics
    """
    dow_stats = ts_data.groupby('day_name').agg({
        'flight_count': ['mean', 'std', 'min', 'max'],
        'cancellation_rate': ['mean', 'std'],
        'avg_air_time': ['mean', 'std'],
        'delay_intensity': ['mean', 'std'],
        'operational_efficiency': ['mean', 'std']
    }).round(3)
    
    # Flatten column names
    dow_stats.columns = [f"{col[1]}_{col[0]}" for col in dow_stats.columns]
    
    # Reorder by actual day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_stats = dow_stats.reindex([day for day in day_order if day in dow_stats.index])
    
    return dow_stats

def plot_weekly_patterns(ts_data, figsize=(15, 10)):
    """
    Create comprehensive weekly pattern visualizations.
    
    Args:
        ts_data (pd.DataFrame): Time series data
        figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Day of week patterns
    dow_stats = day_of_week_analysis(ts_data)
    
    # Flight count by day of week
    dow_stats['mean_flight_count'].plot(kind='bar', ax=axes[0,0], color='skyblue')
    axes[0,0].set_title('Average Daily Flights by Day of Week')
    axes[0,0].set_ylabel('Average Flights')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Cancellation rate by day of week
    dow_stats['mean_cancellation_rate'].plot(kind='bar', ax=axes[0,1], color='salmon')
    axes[0,1].set_title('Average Cancellation Rate by Day of Week')
    axes[0,1].set_ylabel('Cancellation Rate')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Air time efficiency by day of week
    dow_stats['mean_operational_efficiency'].plot(kind='bar', ax=axes[1,0], color='lightgreen')
    axes[1,0].set_title('Operational Efficiency by Day of Week')
    axes[1,0].set_ylabel('Minutes per 1000 miles')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Delay intensity by day of week
    dow_stats['mean_delay_intensity'].plot(kind='bar', ax=axes[1,1], color='orange')
    axes[1,1].set_title('Average Delay Intensity by Day of Week')
    axes[1,1].set_ylabel('Minutes delay per flight')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('outputs/weekly_patterns_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return dow_stats

def comprehensive_seasonal_analysis():
    """
    Run complete seasonal decomposition analysis pipeline.
    
    Returns:
        dict: Complete analysis results
    """
    print("🛫 Flight Data Seasonal Decomposition Analysis")
    print("=" * 60)
    
    # Load and prepare data
    print("1. Loading and preparing time series data...")
    raw_data = load_flight_data()
    ts_data = prepare_time_series_data(raw_data)
    
    print(f"   ✓ Data prepared: {len(ts_data)} days from {ts_data.index.min().strftime('%Y-%m-%d')} to {ts_data.index.max().strftime('%Y-%m-%d')}")
    
    # Display basic statistics
    print("\n2. Time Series Data Overview:")
    print(ts_data.describe())
    
    # Analyze seasonal patterns
    print("\n3. Performing Seasonal Decomposition Analysis...")
    key_metrics = ['flight_count', 'cancellation_rate', 'avg_air_time', 'delay_intensity']
    decomposition_results = analyze_seasonal_patterns(ts_data, key_metrics)
    
    # Day of week analysis
    print("\n4. Analyzing Day-of-Week Patterns...")
    dow_patterns = plot_weekly_patterns(ts_data)
    print("\nDay of Week Statistics:")
    print(dow_patterns)
    
    # Create summary insights
    insights = generate_seasonal_insights(ts_data, decomposition_results)
    
    results = {
        'time_series_data': ts_data,
        'decomposition_results': decomposition_results,
        'day_of_week_patterns': dow_patterns,
        'insights': insights
    }
    
    print("\n✅ Analysis complete! Visualizations saved to 'outputs/' directory")
    
    return results

def generate_seasonal_insights(ts_data, decomposition_results):
    """
    Generate key insights from seasonal decomposition analysis.
    
    Args:
        ts_data (pd.DataFrame): Time series data
        decomposition_results (dict): Decomposition results
        
    Returns:
        dict: Key insights and findings
    """
    insights = {}
    
    # Overall trends
    flight_trend = ts_data['flight_count'].diff().mean()
    insights['flight_volume_trend'] = 'Increasing' if flight_trend > 0 else 'Decreasing'
    
    # Day of week patterns
    dow_flight_pattern = ts_data.groupby('day_name')['flight_count'].mean()
    busiest_day = dow_flight_pattern.idxmax()
    quietest_day = dow_flight_pattern.idxmin()
    
    insights['busiest_day'] = busiest_day
    insights['quietest_day'] = quietest_day
    insights['weekend_vs_weekday'] = {
        'weekend_avg': ts_data[ts_data['is_weekend']]['flight_count'].mean(),
        'weekday_avg': ts_data[~ts_data['is_weekend']]['flight_count'].mean()
    }
    
    # Operational patterns
    insights['cancellation_patterns'] = {
        'highest_cancellation_day': ts_data.groupby('day_name')['cancellation_rate'].mean().idxmax(),
        'overall_cancellation_rate': ts_data['cancellation_rate'].mean()
    }
    
    return insights

# Example usage and main execution
if __name__ == "__main__":
    # Run comprehensive analysis
    results = comprehensive_seasonal_analysis()