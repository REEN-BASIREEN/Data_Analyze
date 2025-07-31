import pandas as pd
import matplotlib.pyplot as plt

# Read PPG Rate from 5min_addtime_with_rate.csv
ppg_df = pd.read_csv('5min_addtime_with_rate.csv')

# Read My sensor from data_calibate.xlsx and process it
sensor_df = pd.read_excel('data_calibate.xlsx')
print("\nSensor data columns:", sensor_df.columns.tolist())
print("\nFirst few rows of sensor data:\n", sensor_df.head())

# แปลง Timestamp ของ PPG เป็น datetime
ppg_df['Timestamp'] = pd.to_datetime(ppg_df['Timestamp'])

# เตรียมข้อมูล sensor
sensor_values = [95,95,95,95,95,97,92,92,92,93,93,93,92,92,91,91,91,91,96,96,94,94,
                96,96,96,96,84,94,90,90,91,91,88,88,88,88,88,88,88,88,87,87,90,90,
                92,92,93,93,93,93,94,94,92,92,92,91,91,90,90,91,91,90,90,91,91,91,
                92,91,92,95,95,98,98,100,100,101,101,102,102,100,100,98,87,100,100,
                98,98,98,98,100,100,98,98,95,95,95,95,94,94,94,94,93,93,93,93,94,94,
                96,96,94,94,95,95,95,95,100,100,102,102,103,103,108,108,110,110,105,
                105,107,107,108,108,108,105,105,107,107,107,107,105,105,105,105,105,
                105,101,101,101,101,100,100,101]

# กำหนดเวลาเริ่มต้นเดียวกับ PPG (11:42:47)
start_time = pd.to_datetime('2025-07-26 11:42:47')
time_seconds = list(range(0, len(sensor_values) * 2, 2))
timestamps = [start_time + pd.Timedelta(seconds=s) for s in time_seconds]

# สร้าง DataFrame ใหม่
sensor_df_valid = pd.DataFrame({
    'Timestamp': timestamps,
    'My sensor': sensor_values
})

print("\nValid sensor data:")
print("Shape:", sensor_df_valid.shape)
print("Sample data:\n", sensor_df_valid.head())



# ใช้ timestamp จาก 5min_addtime_with_rate.csv เป็นแกน x หลัก
timestamp = ppg_df['Timestamp']
ppg_rate = ppg_df['PPG_Rate']

# ตรวจสอบและ print ข้อมูลเพื่อดูค่า
print("PPG Timestamp range:", ppg_df['Timestamp'].min(), "to", ppg_df['Timestamp'].max())
print("Sensor Timestamp range:", sensor_df_valid['Timestamp'].min(), "to", sensor_df_valid['Timestamp'].max())
print("Number of PPG data points:", len(ppg_df))
print("Number of Sensor data points:", len(sensor_df_valid))

# กรองข้อมูล PPG เฉพาะช่วงเวลาที่ต้องการ
mask = (ppg_df['Timestamp'] >= start_time) & (ppg_df['Timestamp'] <= timestamps[-1])
ppg_filtered = ppg_df[mask]

# Resample PPG rate ให้เป็นทุก 2 วินาที
ppg_resampled = ppg_filtered.set_index('Timestamp').resample('2S').mean().reset_index()
ppg_timestamp = ppg_resampled['Timestamp']
ppg_rate = ppg_resampled['PPG_Rate'].round()  # ปัดเศษให้เป็นจำนวนเต็ม

# ใช้ข้อมูลจาก sensor_df_valid
sensor_timestamp = sensor_df_valid['Timestamp']
my_sensor = sensor_df_valid['My sensor']

print("\nPPG Rate range:", ppg_rate.min(), "to", ppg_rate.max())
print("My sensor range:", my_sensor.min(), "to", my_sensor.max())

import matplotlib.dates as mdates

plt.figure(figsize=(14, 6))
# Plot My sensor (without markers)
plt.plot(sensor_timestamp, my_sensor, 'b-', label='Raw Sensor', linewidth=1.5)
# Plot PPG rate (without markers)
plt.plot(ppg_timestamp, ppg_rate, 'orange', label='Reference', linewidth=1, alpha=0.7)

plt.grid(True, linestyle='--', alpha=0.3)
plt.xlabel('Time')
plt.ylabel('Heart Rate (BPM)')
plt.title('Time Series Comparison')
plt.legend(frameon=True, loc='upper right')
plt.ylim(75, 115)  # ปรับช่วงแกน y ให้เหมาะสม

# ปรับรูปแบบแกน x เป็น HH:MM:SS และแสดงวินาที
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=30))  # แสดงเลขทุก 30 วินาที
plt.gcf().autofmt_xdate()

# เพิ่ม grid แนวตั้งเพื่อให้ดูวินาทีได้ง่ายขึ้น
plt.grid(True, which='major', axis='x', linestyle='-', alpha=0.3)

plt.tight_layout()
plt.show()
