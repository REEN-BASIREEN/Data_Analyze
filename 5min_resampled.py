import neurokit2 as nk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read PPG data from CSV file (assume 2nd column is PPG, 1st column is time)
df = pd.read_csv("5min.csv")
print("Available columns:", df.columns.tolist())
ppg_data = df.iloc[:, 1].values
time_data = df.iloc[:, 0].values

# Set your actual sampling rate here (Hz)
sampling_rate = 151

# Process the PPG signal
signals, info = nk.ppg_process(ppg_data, sampling_rate=sampling_rate)

# Extract PPG rate (BPM)
ppg_rate = signals["PPG_Rate"].values
time = signals.index.values / sampling_rate  # convert index to seconds

print(f"Average PPG Rate: {np.nanmean(ppg_rate):.2f} BPM")
print(f"Min PPG Rate: {np.nanmin(ppg_rate):.2f} BPM")
print(f"Max PPG Rate: {np.nanmax(ppg_rate):.2f} BPM")

# Plot the PPG signal and PPG rate
fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
axs[0].plot(time, signals["PPG_Clean"], label="PPG Clean")
axs[0].set_ylabel("Amplitude")
axs[0].set_title("Cleaned PPG Signal")
axs[0].legend()

axs[1].plot(time, ppg_rate, label="PPG Rate (BPM)")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Rate (BPM)")
axs[1].set_title("PPG Rate Over Time")
axs[1].legend()

plt.tight_layout()
plt.show()



import neurokit2 as nk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




# Read PPG data from data_calibate.xlsx (column 'My sensor')
df = pd.read_excel("data_calibate.xlsx")
print("Available columns:", df.columns.tolist())

print("Available columns:", df.columns.tolist())
if 'My sensor' not in df.columns:
    raise ValueError("Column 'My sensor' not found in data_calibate.xlsx")
# Convert to numeric and drop NaN
ppg_data = pd.to_numeric(df['My sensor'], errors='coerce').dropna().values

# Set your actual sampling rate here (Hz)
sampling_rate = 151  # ปรับตามจริงถ้าจำเป็น



# --- Plot comparison between data_calibate.xlsx and 5min_resampled.csv ---
# Read resampled PPG data
df_resampled = pd.read_csv("5min_resampled.csv")
time_resampled = df_resampled['Time'].values
ppg_resampled = df_resampled['PPG_Resampled'].values

plt.figure(figsize=(12, 6))
plt.plot(time_resampled, ppg_resampled, marker='o', label='PPG from 5min.csv (resampled)')
plt.plot(np.arange(len(ppg_data))*2, ppg_data, marker='x', label='My sensor (data_calibate.xlsx)')
plt.xlabel('Time (s)')
plt.ylabel('PPG Rate (BPM)')
plt.title('Comparison of PPG Rate: 5min.csv (resampled) vs My sensor (data_calibate.xlsx)')
plt.legend()
plt.tight_layout()
plt.show()
