import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data():
    """Load data from PPG file and sensor data"""
    # Read PPG data
    ppg_df = pd.read_csv('5min_addtime_with_rate.csv')
    ppg_df['Timestamp'] = pd.to_datetime(ppg_df['Timestamp'])
    
    # Read sensor data from Excel file
    sensor_df = pd.read_excel('data_calibate.xlsx')
    # Convert time_stamp to datetime
    sensor_df['Timestamp'] = pd.Timestamp('2025-07-26 11:42:47') + pd.to_timedelta(sensor_df.index * 2, unit='s')
    
    return ppg_df, sensor_df

def process_data(ppg_df, sensor_df):
    """Process and format data for analysis"""
    # Set fixed start time at 11:42:47
    start_time = pd.Timestamp('2025-07-26 11:42:47')
    end_time = start_time + pd.Timedelta(minutes=5)  # 5 minutes duration
    
    # Filter PPG data for the specified time range
    mask = (ppg_df['Timestamp'] >= start_time) & (ppg_df['Timestamp'] <= end_time)
    ppg_filtered = ppg_df[mask]
    
    # Resample PPG data to 2-second intervals
    ppg_resampled = ppg_filtered.set_index('Timestamp').resample('2s').mean().reset_index()
    ppg_resampled['PPG_Rate'] = ppg_resampled['PPG_Rate'].round()
    
    return ppg_resampled, sensor_df

def calculate_statistics(sensor_data, ppg_data):
    """Calculate statistical metrics"""
    stats = {
        'Raw Sensor': {
            'min': sensor_data['My sensor'].min(),
            'max': sensor_data['My sensor'].max(),
            'mean': sensor_data['My sensor'].mean(),
            'std': sensor_data['My sensor'].std()
        },
        'Reference': {
            'min': ppg_data['PPG_Rate'].min(),
            'max': ppg_data['PPG_Rate'].max(),
            'mean': ppg_data['PPG_Rate'].mean(),
            'std': ppg_data['PPG_Rate'].std()
        }
    }
    
    # Calculate error metrics
    errors = {
        'Mean Absolute Error': abs(stats['Raw Sensor']['mean'] - stats['Reference']['mean']),
        'Max Error': abs(stats['Raw Sensor']['max'] - stats['Reference']['max']),
        'Min Error': abs(stats['Raw Sensor']['min'] - stats['Reference']['min']),
        'SD Difference': abs(stats['Raw Sensor']['std'] - stats['Reference']['std'])
    }
    
    return stats, errors

def print_statistics(stats, errors):
    """Display statistical results and error metrics"""
    print("\n=== Statistical Analysis ===")
    for sensor_type, values in stats.items():
        print(f"\n{sensor_type}:")
        print(f"Minimum: {values['min']:.2f} BPM")
        print(f"Maximum: {values['max']:.2f} BPM")
        print(f"Mean: {values['mean']:.2f} BPM")
        print(f"Standard Deviation: {values['std']:.2f} BPM")

    print("\n=== Error Analysis ===")
    for error_type, value in errors.items():
        print(f"{error_type}: {value:.2f} BPM")

def plot_comparison(sensor_df, ppg_df, stats):
    """Create comparison plots for time series and statistics"""
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[2, 1])
    
    # Plot time series
    ax1.plot(sensor_df['Timestamp'], sensor_df['My sensor'], 'b-', 
             label='Raw Sensor', linewidth=1.5)
    ax1.plot(ppg_df['Timestamp'], ppg_df['PPG_Rate'], 'orange', 
             label='Reference', linewidth=1, alpha=0.7)
    
    # Format time series plot
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Heart Rate (BPM)')
    ax1.set_title('Heart Rate Time Series Comparison')
    ax1.legend(frameon=True, loc='upper right')
    ax1.set_ylim(75, 115)
    
    # Format time axis to show time since start
    start_time = pd.Timestamp('2025-07-26 11:42:47')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
    
    # Set x-axis limits to show exactly from start time
    ax1.set_xlim(start_time, start_time + pd.Timedelta(minutes=5))
    
    # Plot statistical comparison
    metrics = ['min', 'max', 'mean', 'std']
    labels = ['Min', 'Max', 'Mean', 'SD']
    raw_values = [stats['Raw Sensor'][k] for k in metrics]
    ref_values = [stats['Reference'][k] for k in metrics]
    
    x = range(len(metrics))
    width = 0.35
    
    # Create bar chart
    ax2.bar([i - width/2 for i in x], raw_values, width, 
            label='Raw Sensor', color='blue', alpha=0.7)
    ax2.bar([i + width/2 for i in x], ref_values, width, 
            label='Reference', color='orange', alpha=0.7)
    
    # Add value labels on bars
    for i, v in enumerate(raw_values):
        ax2.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
    for i, v in enumerate(ref_values):
        ax2.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')
    
    # Format statistical plot
    ax2.set_ylabel('BPM')
    ax2.set_title('Statistical Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    # Load data
    ppg_df, sensor_df = load_data()
    
    # Process data
    ppg_processed, sensor_processed = process_data(ppg_df, sensor_df)
    
    # Calculate statistics
    stats, errors = calculate_statistics(sensor_processed, ppg_processed)
    
    # Display statistics
    print_statistics(stats, errors)
    
    # Create and display plots
    fig = plot_comparison(sensor_processed, ppg_processed, stats)
    plt.show()

if __name__ == "__main__":
    main()
