import neurokit2 as nk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd






# Read PPG data from Calibration.xlsx (columns 'Sensor' and 'Biopac')
df = pd.read_excel("Calibration.xlsx")
print("Available columns:", df.columns.tolist())

if not all(col in df.columns for col in ['Timestamp', 'Sensor', 'Biopac']):
    raise ValueError("Columns 'Timestamp', 'Sensor', or 'Biopac' not found in Calibration.xlsx")

# Create proper timestamp starting from 11:42:57
start_time = pd.Timestamp('2025-07-26 11:42:57')
df['Timestamp'] = pd.date_range(start=start_time, periods=len(df), freq='10s')

# Convert to numeric and drop NaN for both columns
sensor_data = pd.to_numeric(df['Sensor'], errors='coerce')
biopac_data = pd.to_numeric(df['Biopac'], errors='coerce')
timestamp = df['Timestamp']

# Plot comparison between Sensor and Biopac
plt.figure(figsize=(14, 6))
plt.plot(timestamp, sensor_data, marker='o', label='Sensor')
plt.plot(timestamp, biopac_data, marker='x', label='Biopac')
plt.xlabel('Time')
plt.ylabel('Heart Rate (BPM)')
plt.title('Comparison: Heart Rate (Sensor vs Biopac) from Calibration.xlsx')
plt.legend()

# Format time axis to show HH:MM:SS
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=30))  # แสดงเลขทุก 30 วินาที

# Set specific x-axis limits from 11:42:57 to 11:47:47
start_time = pd.Timestamp('2025-07-26 11:42:57')
end_time = pd.Timestamp('2025-07-26 11:47:47')
plt.xlim(start_time, end_time)

plt.tight_layout()
plt.show()
