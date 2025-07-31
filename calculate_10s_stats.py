import pandas as pd

# อ่านข้อมูลจากไฟล์
df = pd.read_csv('5min_addtime_with_rate.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# กำหนดเวลาเริ่มต้น
start_time = pd.Timestamp('2025-07-26 11:42:47')
end_time = start_time + pd.Timedelta(minutes=5)

# กรองข้อมูลในช่วงเวลาที่ต้องการ
mask = (df['Timestamp'] >= start_time) & (df['Timestamp'] <= end_time)
df_filtered = df[mask]

# จัดกลุ่มข้อมูลทุก 10 วินาที และคำนวณค่าสถิติ
df_resampled = df_filtered.set_index('Timestamp').resample('10S').agg({
    'PPG_Rate': ['mean', 'min', 'max']
}).round(2)

# ปรับรูปแบบคอลัมน์
df_resampled.columns = ['Mean_Rate', 'Min_Rate', 'Max_Rate']
df_resampled = df_resampled.reset_index()

# บันทึกผลลัพธ์
df_resampled.to_csv('every10second_attime.csv', index=False)

# แสดงผลลัพธ์
print("\nAnalysis of PPG Rate every 10 seconds:")
print("\nFirst few records:")
print(df_resampled.head())

print("\nSummary statistics:")
print("\nOverall statistics:")
print(f"Mean Rate range: {df_resampled['Mean_Rate'].min():.2f} to {df_resampled['Mean_Rate'].max():.2f}")
print(f"Absolute Min: {df_resampled['Min_Rate'].min():.2f}")
print(f"Absolute Max: {df_resampled['Max_Rate'].max():.2f}")

# แสดงจำนวนตัวอย่างที่วิเคราะห์
print(f"\nTotal 10-second intervals analyzed: {len(df_resampled)}")
