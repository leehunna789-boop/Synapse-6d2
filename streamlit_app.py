import streamlit as st
import serial
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Sound Level Monitor", layout="wide")
st.title("🔊 ระบบวัดระดับเสียงและความแม่นยำ")

# ใช้ st.cache_resource เพื่อให้เชื่อมต่อ Serial ค้างไว้แม้จะ Refresh หน้าจอ
@st.cache_resource
def get_serial_connection(port, baudrate):
    try:
        return serial.Serial(port, baudrate, timeout=0.1)
    except Exception as e:
        st.error(f"เชื่อมต่อไม่ได้: {e}")
        return None

ser = get_serial_connection('COM3', 9600)

# สร้างพื้นที่สำหรับแสดงผล
col1, col2 = st.columns([1, 3])
with col1:
    metric_placeholder = st.empty()
with col2:
    chart_placeholder = st.empty()

# เก็บข้อมูลสำหรับทำกราฟ
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Level'])

if ser and ser.is_open:
    st.sidebar.success("สถานะ: เชื่อมต่อแล้ว")
    
    # ปุ่มหยุดการทำงาน
    stop_btn = st.sidebar.button("หยุดการทำงาน")
    
    while not stop_btn:
        line = ser.readline().decode('utf-8').strip()
        
        if line:
            try:
                # แปลงค่าที่รับมาเป็นตัวเลข (สมมติว่าเป็นค่าระดับเสียง)
                value = float(line)
                now = datetime.now().strftime("%H:%M:%S")
                
                # อัปเดต Metric
                metric_placeholder.metric(label="ระดับเสียงปัจจุบัน", value=f"{value} dB")
                
                # อัปเดต Data สำหรับกราฟ (เก็บ 50 ค่าล่าสุด)
                new_data = pd.DataFrame({'Time': [now], 'Level': [value]})
                st.session_state.history = pd.concat([st.session_state.history, new_data]).tail(50)
                
                # แสดงกราฟ
                chart_placeholder.line_chart(st.session_state.history.set_index('Time'))
                
            except ValueError:
                st.warning(f"ข้อมูลผิดพลาด: {line}")
        
        time.sleep(0.05) # ปรับค่าให้เหมาะสมกับความเร็วการส่งข้อมูลจาก Arduino
else:
    st.error("กรุณาตรวจสอบการเชื่อมต่อ Arduino ที่ COM3")
    st.info("คำแนะนำ: ตรวจสอบใน Device Manager ว่า Arduino ใช้ Port อะไร")
