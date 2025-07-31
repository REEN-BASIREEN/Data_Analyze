import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data():
    """Load data from PPG file and sensor data"""
    # อ่านข้อมูล PPG
    ppg_df = pd.read_csv('5min_addtime_with_rate.csv')
    ppg_df['Timestamp'] = pd.to_datetime(ppg_df['Timestamp'])
    
    # สร้างข้อมูล sensor
    sensor_values = [95,95,95,95,95,97,92,92,92,93,93,93,92,92,91,91,91,91,96,96,94,94,
                    96,96,96,96,84,94,90,90,91,91,88,88,88,88,88,88,88,88,87,87,90,90,
                    92,92,93,93,93,93,94,94,92,92,92,91,91,90,90,91,91,90,90,91,91,91,
                    92,91,92,95,95,98,98,100,100,101,101,102,102,100,100,98,87,100,100,
                    98,98,98,98,100,100,98,98,95,95,95,95,94,94,94,94,93,93,93,93,94,94,
                    96,96,94,94,95,95,95,95,100,100,102,102,103,103,108,108,110,110,105,
                    105,107,107,108,108,108,105,105,107,107,107,107,105,105,105,105,105,
                    105,101,101,101,101,100,100,101]
    
    # สร้าง timestamps สำหรับ sensor (เริ่มจาก 11:42:47 ทุกๆ 2 วินาที)
    start_time = pd.to_datetime('2025-07-26 11:42:47')
    time_seconds = range(0, len(sensor_values) * 2, 2)
    timestamps = [start_time + pd.Timedelta(seconds=s) for s in time_seconds]
    
    # สร้าง DataFrame สำหรับ sensor
    sensor_df = pd.DataFrame({
        'Timestamp': timestamps,
        'My sensor': sensor_values
    })
    
    return ppg_df, sensor_df

def process_data(ppg_df, sensor_df):
    """Process and format data for analysis"""
    # กรองข้อมูล PPG ตามช่วงเวลาของ sensor
    start_time = sensor_df['Timestamp'].min()
    end_time = sensor_df['Timestamp'].max()
    mask = (ppg_df['Timestamp'] >= start_time) & (ppg_df['Timestamp'] <= end_time)
    ppg_filtered = ppg_df[mask]
    
    # Resample PPG data ให้เป็นทุก 2 วินาที
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
    
    # คำนวณค่าความคลาดเคลื่อน
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

def create_comparison_plot(sensor_df, ppg_df, stats):
    """Create comparison plots for time series and statistics"""
    # สร้าง subplot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[2, 1])
    
    # Plot time series
    ax1.plot(sensor_df['Timestamp'], sensor_df['My sensor'], 'b-', 
             label='Raw Sensor', linewidth=1.5)
    ax1.plot(ppg_df['Timestamp'], ppg_df['PPG_Rate'], 'orange', 
             label='Reference', linewidth=1, alpha=0.7)
    
    # จัดรูปแบบ time series plot
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Heart Rate (BPM)')
    ax1.set_title('Heart Rate Time Series Comparison')
    ax1.legend(frameon=True, loc='upper right')
    ax1.set_ylim(75, 115)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
    
    # Plot statistical comparison
    metrics = ['min', 'max', 'mean', 'std']
    labels = ['Min', 'Max', 'Mean', 'SD']
    raw_values = [stats['Raw Sensor'][k] for k in metrics]
    ref_values = [stats['Reference'][k] for k in metrics]
    
    x = range(len(metrics))
    width = 0.35
    
    # สร้าง bar chart
    ax2.bar([i - width/2 for i in x], raw_values, width, 
            label='Raw Sensor', color='blue', alpha=0.7)
    ax2.bar([i + width/2 for i in x], ref_values, width, 
            label='Reference', color='orange', alpha=0.7)
    
    # เพิ่มค่าตัวเลขบนแท่ง
    for i, v in enumerate(raw_values):
        ax2.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
    for i, v in enumerate(ref_values):
        ax2.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')
    
    # จัดรูปแบบ statistical plot
    ax2.set_ylabel('BPM')
    ax2.set_title('Statistical Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    return fig

def main():
    # โหลดข้อมูล
    ppg_df, sensor_df = load_data()
    
    # ประมวลผลข้อมูล
    ppg_processed, sensor_processed = process_data(ppg_df, sensor_df)
    
    # คำนวณค่าสถิติ
    stats, errors = calculate_statistics(sensor_processed, ppg_processed)
    
    # แสดงผลค่าสถิติ
    print_statistics(stats, errors)
    
    # สร้างและแสดงกราฟ
    fig = create_comparison_plot(sensor_processed, ppg_processed, stats)
    plt.show()

if __name__ == "__main__":
    main()
