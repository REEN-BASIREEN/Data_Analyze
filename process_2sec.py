import pandas as pd
import numpy as np

# อ่านไฟล์ CSV
df = pd.read_csv(r'c:\Users\satit\OneDrive\เดสก์ท็อป\Personal Monitor\calibration_data.csv')

# สร้างช่วงเวลาใหม่ที่มีระยะห่างเท่ากัน
start_time = df['Time (s)'].min()
end_time = df['Time (s)'].max()
num_points = 150  # จำนวนจุดที่ต้องการ
new_times = np.linspace(start_time, end_time, num_points)

# สร้างฟังก์ชันสำหรับหาค่าเฉลี่ยรอบๆ แต่ละจุดเวลา
def get_averaged_values(df, times, window_size=1.0):
    result_data = []
    for t in times:
        # หาข้อมูลในช่วง window_size วินาทีรอบๆ เวลาที่สนใจ
        mask = (df['Time (s)'] >= t - window_size/2) & (df['Time (s)'] <= t + window_size/2)
        window_data = df[mask]
        
        # ถ้าไม่มีข้อมูลในช่วง ให้ใช้ข้อมูลที่ใกล้ที่สุด
        if len(window_data) == 0:
            closest_idx = (df['Time (s)'] - t).abs().idxmin()
            window_data = df.iloc[[closest_idx]]
        
        result_data.append({
            'Time (s)': t,
            'Heart_Rate (BPM)': window_data['Heart_Rate (BPM)'].mean(),
            'Raw_Signal': window_data['Raw_Signal'].mean(),
            'Filtered_Signal': window_data['Filtered_Signal'].mean()
        })
    
    return pd.DataFrame(result_data)

# ประมวลผลข้อมูล
processed_df = get_averaged_values(df, new_times)

# บันทึกลงไฟล์ CSV
processed_df.to_csv('calibration_data.csv', index=False)

print(f"บันทึกข้อมูลเรียบร้อยแล้ว")
print(f"จำนวนข้อมูลที่เก็บได้: {len(processed_df)} ค่า")
print(f"ช่วงเวลาระหว่างแต่ละจุด: {(end_time - start_time) / (num_points - 1):.2f} วินาที")
print("\nตัวอย่าง 5 ค่าแรก:")
print(processed_df.head())

interval = (end_time - start_time) / (num_points - 1)
print(f"บันทึกข้อมูลเรียบร้อยแล้ว")
print(f"จำนวนข้อมูลที่เก็บได้: {len(processed_df)} ค่า")
print(f"ช่วงเวลาระหว่างแต่ละจุด: {interval:.2f} วินาที")
print("\nตัวอย่าง 5 ค่าแรก:")
print(processed_df.head())
