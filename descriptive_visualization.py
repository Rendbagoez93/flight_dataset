import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path

from data_preprocess import perform_complete_analysis, preprocess_flight_data

# Set visualization style
sns.set(style="whitegrid", palette="pastel")
plt.rcParams['figure.figsize'] = (10, 6)

# Create outputs folder for saved plots
Path('outputs').mkdir(parents=True, exist_ok=True)

# Silence warnings in visualization output
warnings.filterwarnings('ignore')

# Visualization functions
def visualize_flights_by_time(time_analysis):
    """Visualize flights by day of week and month with enhanced styling"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Day of week plot with proper ordering
    order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    flights_per_dow = time_analysis['flights_per_dow']
    if hasattr(flights_per_dow.index[0], 'startswith') and any(day in str(flights_per_dow.index[0]) for day in order):
        # Handle day names if they exist
        flights_per_dow = flights_per_dow.reindex(order, fill_value=0)
    
    sns.barplot(x=flights_per_dow.index, 
                y=flights_per_dow.values, 
                palette='viridis', ax=ax1)
    ax1.set_title("Flights by Day of Week")
    ax1.set_xlabel("Day of Week")
    ax1.set_ylabel("Number of Flights")
    ax1.tick_params(axis='x', rotation=45)
    
    # Month plot
    sns.barplot(x=time_analysis['flights_per_month'].index, 
                y=time_analysis['flights_per_month'].values, 
                palette='coolwarm', ax=ax2)
    ax2.set_title("Flights by Month")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Number of Flights")
    
    plt.tight_layout()
    plt.savefig('outputs/flights_by_dow.png', dpi=150, bbox_inches='tight')
    plt.show()
    
def visualize_flights_by_airport(airport_analysis):
    """Visualize flights by origin airport (top 10)"""
    plt.figure(figsize=(12, 6))
    # Show only top 10 airports for better readability
    top_airports = airport_analysis.head(10)
    sns.barplot(x=top_airports.index, y=top_airports.values, palette='magma')
    plt.title("Top 10 Origin Airports by Flight Count")
    plt.xlabel("Origin Airport")
    plt.ylabel("Number of Flights")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/flights_by_airport.png', dpi=150, bbox_inches='tight')
    plt.show()
    
def visualize_cancellations(cancellation_analysis):
    """Visualize cancellation patterns"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Cancellations by month
    cancel_by_month = cancellation_analysis['cancel_by_month']
    if not cancel_by_month.empty:
        sns.barplot(x=cancel_by_month.index, y=cancel_by_month.values, 
                   palette='coolwarm', ax=ax1)
        ax1.set_title("Cancellations by Month")
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Number of Cancellations")
    
    # Cancellations by origin (top 10)
    cancel_by_origin = cancellation_analysis['cancel_by_origin'].head(10)
    if not cancel_by_origin.empty:
        sns.barplot(x=cancel_by_origin.index, y=cancel_by_origin.values, 
                   palette='Reds', ax=ax2)
        ax2.set_title("Top 10 Airports by Cancellations")
        ax2.set_xlabel("Origin Airport")
        ax2.set_ylabel("Number of Cancellations")
        ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('outputs/cancellation_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

def visualize_flight_duration_distance(duration_analysis):
    """Visualize flight duration and distance statistics"""
    plt.figure(figsize=(12, 8))
    
    # Create heatmap of the statistics
    sns.heatmap(duration_analysis, annot=True, cmap='YlOrRd', fmt='.1f')
    plt.title("Flight Duration and Distance Statistics")
    plt.xlabel("Metrics")
    plt.ylabel("Statistics")
    plt.tight_layout()
    plt.savefig('outputs/duration_distance_heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()
    
def visualize_delays(delay_analysis):
    """Visualize delay statistics"""
    plt.figure(figsize=(12, 6))
    
    delay_summary = delay_analysis['delay_summary']
    sns.heatmap(delay_summary, annot=True, cmap='Reds', fmt='.1f')
    plt.title("Delay Statistics Heatmap")
    plt.xlabel("Delay Types")
    plt.ylabel("Statistics")
    plt.tight_layout()
    plt.savefig('outputs/delay_heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()

def visualize_airport_performance(airport_performance):
    """Visualize airport performance metrics"""
    plt.figure(figsize=(14, 8))
    
    # Show top 10 airports by weather delay
    top_airports = airport_performance.head(10)
    
    # Create subplots for different metrics
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Air time
    sns.barplot(data=top_airports.reset_index(), x='origin', y='air_time', 
                palette='Blues', ax=axes[0,0])
    axes[0,0].set_title('Average Air Time by Airport')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Taxi out time
    sns.barplot(data=top_airports.reset_index(), x='origin', y='taxi_out', 
                palette='Greens', ax=axes[0,1])
    axes[0,1].set_title('Average Taxi Out Time by Airport')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Weather delay
    sns.barplot(data=top_airports.reset_index(), x='origin', y='weather_delay', 
                palette='Oranges', ax=axes[1,0])
    axes[1,0].set_title('Average Weather Delay by Airport')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Late aircraft delay
    sns.barplot(data=top_airports.reset_index(), x='origin', y='late_aircraft_delay', 
                palette='Reds', ax=axes[1,1])
    axes[1,1].set_title('Average Late Aircraft Delay by Airport')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

def visualize_monthly_delays(monthly_delays):
    """Visualize monthly delay patterns"""
    plt.figure(figsize=(12, 6))
    
    monthly_delays.plot(kind='bar', figsize=(12, 6), color=['skyblue', 'lightcoral'])
    plt.title("Average Monthly Delays")
    plt.xlabel("Month")
    plt.ylabel("Average Delay (minutes)")
    plt.legend(['Weather Delay', 'Late Aircraft Delay'])
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('outputs/monthly_delays_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    
def visualize_complete_analysis(analysis_results):
    """Generate all visualizations from analysis results"""
    print("Generating visualizations...")
    
    visualize_flights_by_time(analysis_results['time_analysis'])
    visualize_flights_by_airport(analysis_results['airport_analysis'])
    visualize_cancellations(analysis_results['cancellation_analysis'])
    visualize_flight_duration_distance(analysis_results['duration_analysis'])
    visualize_delays(analysis_results['delay_analysis'])
    visualize_airport_performance(analysis_results['airport_performance'])
    visualize_monthly_delays(analysis_results['monthly_delays'])
    
    return "All visualizations generated successfully."

if __name__ == "__main__":
    # Run the complete visualization pipeline
    file_path = 'data/flight_data_2024.csv'
    processed_df = preprocess_flight_data(file_path, verbose=False)
    
    print("\n" + "="*50)
    print("DESCRIPTIVE ANALYSIS VISUALIZATION")
    print("="*50)
    
    # Perform descriptive analysis
    analysis_results = perform_complete_analysis(processed_df)
    
    # Generate visualizations
    result = visualize_complete_analysis(analysis_results)
    print(f"\n{result}")