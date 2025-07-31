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
ppg_data = pd.to_numeric(df['My sensor'], errors='coerce')

# เลือกเฉพาะแถวที่เวลาเป็น 4, 10, 14, 20, 24,... วินาที
if 'Time' in df.columns:
    time_col = df['Time']
else:
    # ถ้าไม่มีคอลัมน์ Time ให้สร้างเอง (สมมติเริ่มที่ 0, sampling_rate = 60 Hz)
    sampling_rate = 60  # ปรับตามจริงถ้าจำเป็น
    time_col = np.arange(len(df)) * (1/sampling_rate)

select_times = np.arange(4, time_col.max()+1, 4)
mask = np.isin(time_col, select_times)
df_selected = df.loc[mask]
df_selected.to_csv('every5second_mysensor.csv', index=False)
print('Saved selected data to every5second_mysensor.csv')

# Plot the PPG rate from 'My sensor' column directly
plt.figure(figsize=(12, 4))
plt.plot(ppg_data.values, label='My sensor (PPG Rate)')
plt.xlabel('Sample')
plt.ylabel('PPG Rate (BPM)')
plt.title('PPG Rate from My sensor (data_calibate.xlsx)')
plt.legend()
plt.tight_layout()
plt.show()
