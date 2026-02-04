import streamlit as st
import serial
import time
from datetime import datetime

st.title("ระบบวัดระดับเสียงและความแม่นยำ")

# ตั้งค่าพอร์ต (เปลี่ยน 'COM3' เป็นพอร์ตที่ Arduino ต่ออยู่)
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    st.success("เชื่อมต่อ Arduino สำเร็จ")
except:
    st.error("ไม่สามารถเชื่อมต่อ Arduino ได้ กรุณาเช็คพอร์ต COM")

placeholder = st.empty()

while True:
    if 'ser' in locals() and ser.is_open:
        # อ่านข้อมูลจาก Arduino
        line = ser.readline().decode('utf-8').strip()
        
        if line:
            with placeholder.container():
                # แสดงเวลาจากฝั่งคอมพิวเตอร์ควบคู่ไปด้วยเพื่อความแม่นยำ
                current_time = datetime.now().strftime("%H:%M:%S")
                
                st.metric(label="เวลาปัจจุบัน (System)", value=current_time)
                st.info(f"ข้อมูลจากอุปกรณ์: {line}")
                
                # ทำกราฟ Real-time (ถ้าต้องการ)
                # st.line_chart(...) 

    time.sleep(0.1)
