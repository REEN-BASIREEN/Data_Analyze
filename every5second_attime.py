import neurokit2 as nk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Read PPG data from CSV file (assume 2nd column is PPG, 1st column is time)
df = pd.read_excel("5min_addtime.xlsx")
print("Available columns:", df.columns.tolist())
ppg_data = df.iloc[:, 1].values
time_data = df.iloc[:, 0].values

# Extract data every 5 seconds
interval = 10  # seconds
sampling_rate = 500  # Hz (0.005s per sample)
step = int(interval / 0.005)  # number of samples per 5 seconds
indices = np.arange(0, len(time_data), step)
df_every5s = df.iloc[indices]
df_every5s.to_csv('every10second_attime.csv', index=False)
print('Saved every 5s data to every5second_attime.csv')

# Set your actual sampling rate here (Hz)
sampling_rate = 200

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
