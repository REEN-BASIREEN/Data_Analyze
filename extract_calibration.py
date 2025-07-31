import pandas as pd
import numpy as np
from scipy import stats
from scipy.signal import find_peaks, butter, filtfilt
import matplotlib.pyplot as plt

def extract_calibration_data(csv_file, window_size=200):
    """
    Extract calibration data from PPG signal by averaging every 200 samples
    
    Args:
        csv_file (str): Path to input CSV file containing PPG data
        window_size (int): Number of samples to average for each point
    """
    # Read CSV file
    df = pd.read_csv(csv_file)
    print("Available columns:", df.columns.tolist())
    
    # Get PPG data
    ppg_data = df.iloc[:, 1].values  # PPG column
    time_data = df['Time'].values
    
    # Signal Preprocessing
    fs = 1 / (time_data[1] - time_data[0])  # Sampling frequency
    nyq = fs / 2  # Nyquist frequency
    b, a = butter(3, [0.5/nyq, 5/nyq], btype='band')
    
    # Apply filter
    ppg_filtered = filtfilt(b, a, ppg_data)
    
    # Peak Detection
    peaks, properties = find_peaks(ppg_filtered, 
                                 distance=int(fs/3),
                                 height=np.mean(ppg_filtered),
                                 prominence=0.1)
    
    # Calculate heart rates for entire signal
    peak_times = time_data[peaks]
    peak_intervals = np.diff(peak_times)
    rates = 60 / peak_intervals  # Convert to BPM
    
    # Divide data into windows and calculate average
    num_windows = len(rates) // window_size
    averaged_rates = []
    averaged_times = []
    averaged_raw = []
    averaged_filtered = []
    
    for i in range(num_windows):
        start_idx = i * window_size
        end_idx = (i + 1) * window_size
        
        # Calculate averages for this window
        avg_rate = np.mean(rates[start_idx:end_idx])
        avg_time = np.mean(peak_times[start_idx+1:end_idx+1])  # +1 because rates are calculated from intervals
        avg_raw = np.mean(ppg_data[peaks[start_idx+1:end_idx+1]])
        avg_filtered = np.mean(ppg_filtered[peaks[start_idx+1:end_idx+1]])
        
        averaged_rates.append(avg_rate)
        averaged_times.append(avg_time)
        averaged_raw.append(avg_raw)
        averaged_filtered.append(avg_filtered)
    
    # Prepare calibration data
    calibration_data = {
        'Time (s)': averaged_times,
        'Heart_Rate (BPM)': averaged_rates,
        'Raw_Signal': averaged_raw,
        'Filtered_Signal': averaged_filtered
    }
    
    # Create DataFrame
    cal_df = pd.DataFrame(calibration_data)
    
    # Save to CSV
    output_file = 'calibration_data_averaged.csv'
    cal_df.to_csv(output_file, index=False)
    print(f"\nCalibration data saved to {output_file}")
    print(f"Number of samples saved: {len(cal_df)}")
    
    # Plot the data
    plt.figure(figsize=(15, 15))
    
    # Plot 1: Original heart rates
    plt.subplot(3, 1, 1)
    plt.plot(peak_times[1:], rates, 'b-', alpha=0.5, label='Original measurements')
    plt.title('Original Heart Rate Measurements')
    plt.xlabel('Time (s)')
    plt.ylabel('Heart Rate (BPM)')
    plt.legend()
    
    # Plot 2: Averaged heart rates
    plt.subplot(3, 1, 2)
    plt.plot(cal_df['Time (s)'], cal_df['Heart_Rate (BPM)'], 'r.-', 
             label=f'Averaged every {window_size} points')
    plt.title('Averaged Heart Rate Measurements for Calibration')
    plt.xlabel('Time (s)')
    plt.ylabel('Heart Rate (BPM)')
    plt.legend()
    
    # Plot 3: Distribution of averaged values
    plt.subplot(3, 1, 3)
    plt.hist(cal_df['Heart_Rate (BPM)'], bins=20, edgecolor='black')
    plt.axvline(x=np.mean(cal_df['Heart_Rate (BPM)']), color='r', linestyle='--',
                label=f'Mean: {np.mean(cal_df["Heart_Rate (BPM)"]):.1f} BPM')
    plt.title('Distribution of Averaged Heart Rates')
    plt.xlabel('Heart Rate (BPM)')
    plt.ylabel('Count')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Calculate detailed statistics
    print("\n=== Detailed Statistical Analysis ===")
    
    print("\n1. Original Data Statistics:")
    print(f"Sample Size: {len(rates)}")
    print("\nCentral Tendency:")
    print(f"Mean Heart Rate: {np.mean(rates):.1f} BPM")
    print(f"Median Heart Rate: {np.median(rates):.1f} BPM")
    print(f"Mode Heart Rate: {stats.mode(rates)[0]:.1f} BPM")
    
    print("\nDispersion Measures:")
    print(f"Standard Deviation: {np.std(rates):.2f} BPM")
    print(f"Variance: {np.var(rates):.2f} BPM²")
    print(f"Range: {np.ptp(rates):.2f} BPM")
    print(f"Interquartile Range (IQR): {stats.iqr(rates):.2f} BPM")
    print(f"Minimum: {np.min(rates):.1f} BPM")
    print(f"Maximum: {np.max(rates):.1f} BPM")
    
    print("\nShape Measures:")
    print(f"Skewness: {stats.skew(rates):.3f}")
    print(f"Kurtosis: {stats.kurtosis(rates):.3f}")
    
    print("\nPercentiles:")
    for p in [25, 50, 75, 95]:
        print(f"{p}th percentile: {np.percentile(rates, p):.1f} BPM")
    
    print("\n2. Averaged Data Statistics:")
    print(f"Sample Size: {len(averaged_rates)}")
    print("\nCentral Tendency:")
    print(f"Mean Heart Rate: {np.mean(averaged_rates):.1f} BPM")
    print(f"Median Heart Rate: {np.median(averaged_rates):.1f} BPM")
    print(f"Mode Heart Rate: {stats.mode(averaged_rates)[0]:.1f} BPM")
    
    print("\nDispersion Measures:")
    print(f"Standard Deviation: {np.std(averaged_rates):.2f} BPM")
    print(f"Variance: {np.var(averaged_rates):.2f} BPM²")
    print(f"Range: {np.ptp(averaged_rates):.2f} BPM")
    if len(averaged_rates) >= 4:  # Need at least 4 points for IQR
        print(f"Interquartile Range (IQR): {stats.iqr(averaged_rates):.2f} BPM")
    print(f"Minimum: {np.min(averaged_rates):.1f} BPM")
    print(f"Maximum: {np.max(averaged_rates):.1f} BPM")
    
    if len(averaged_rates) >= 3:  # Need at least 3 points for these statistics
        print("\nShape Measures:")
        print(f"Skewness: {stats.skew(averaged_rates):.3f}")
        print(f"Kurtosis: {stats.kurtosis(averaged_rates):.3f}")
    
    if len(averaged_rates) >= 4:  # Need at least 4 points for percentiles
        print("\nPercentiles:")
        for p in [25, 50, 75, 95]:
            print(f"{p}th percentile: {np.percentile(averaged_rates, p):.1f} BPM")
    
    # Additional analyses
    print("\n3. Additional Analyses:")
    print("\nTime-based Statistics (Original Data):")
    measurement_duration = peak_times[-1] - peak_times[0]
    print(f"Total Duration: {measurement_duration:.1f} seconds")
    print(f"Average Sampling Rate: {len(rates)/measurement_duration:.2f} Hz")
    
    # Calculate heart rate variability metrics
    rr_intervals = np.diff(peak_times) * 1000  # Convert to milliseconds
    print("\nHeart Rate Variability Metrics:")
    print(f"SDNN (Standard Deviation of NN Intervals): {np.std(rr_intervals):.2f} ms")
    print(f"RMSSD (Root Mean Square of Successive Differences): {np.sqrt(np.mean(np.diff(rr_intervals)**2)):.2f} ms")
    print(f"pNN50 (Proportion of NN50): {100 * np.sum(np.abs(np.diff(rr_intervals)) > 50) / len(rr_intervals):.1f}%")
    
    return cal_df

if __name__ == "__main__":
    input_file = "5min.csv"
    calibration_data = extract_calibration_data(input_file, window_size=200)
