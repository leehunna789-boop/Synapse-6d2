import streamlit as st
import serial
import time
from datetime import datetime
import pandas as pd # เพิ่ม pandas สำหรับทำกราฟ

st.set_page_config(page_title="ระบบวัดระดับเสียงและความแม่นยำ", layout="wide")
st.title("🔊 ระบบวัดระดับเสียงและความแม่นยำ")

# ใช้ st.cache_resource เพื่อรักษาการเชื่อมต่อ Serial แม้มีการ Refresh หน้าเว็บ
@st.cache_resource
def get_serial_connection(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        st.success(f"เชื่อมต่อ Arduino สำเร็จที่ {port}")
        return ser
    except Exception as e:
        st.error(f"เชื่อมต่อไม่ได้: [Errno 2] {e}")
        st.info("คำแนะนำ: ตรวจสอบใน Device Manager ว่า Arduino ใช้ Port อะไร")
        return None

# ตั้งค่าพอร์ตและลองเชื่อมต่อ
COM_PORT = 'COM3' # ***แก้ไขตรงนี้เป็นพอร์ตที่ถูกต้อง***
ser = get_serial_connection(COM_PORT, 9600)

# สร้างพื้นที่สำหรับแสดงผลและกราฟ
col1, col2 = st.columns([1, 2])
metric_placeholder = col1.empty()
chart_placeholder = col2.empty()

# เตรียม DataFrame สำหรับเก็บข้อมูลย้อนหลัง 50 ค่า
if 'history_data' not in st.session_state:
    st.session_state.history_data = pd.DataFrame(columns=['Time', 'Level'])

# ปุ่มหยุดการทำงาน (แสดงใน sidebar)
stop_btn = st.sidebar.button("หยุดการทำงาน")

if ser and ser.is_open:
    while not stop_btn:
        try:
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                # แปลงข้อมูลเป็นตัวเลข (สมมติว่าเป็นระดับเสียง)
                try:
                    value = float(line)
                    current_time = datetime.now().strftime("%H:%M:%S")

                    # อัปเดต Metric
                    metric_placeholder.metric(label="ระดับเสียงปัจจุบัน (dB)", value=f"{value:.2f}")

                    # อัปเดตข้อมูลและกราฟ
                    new_row = pd.DataFrame({'Time': [current_time], 'Level': [value]})
                    st.session_state.history_data = pd.concat([st.session_state.history_data, new_row]).tail(50)
                    chart_placeholder.line_chart(st.session_state.history_data.set_index('Time'))
                
                except ValueError:
                    st.warning(f"ได้รับข้อมูลที่ไม่ใช่ตัวเลข: {line}")
            
            time.sleep(0.05) # หน่วงเวลาเล็กน้อย
            
        except serial.SerialException as e:
            st.error(f"การเชื่อมต่อขาดหาย: {e}")
            break # ออกจาก while loop หากเกิดปัญหาการสื่อสาร
    
    # ปิดการเชื่อมต่อเมื่อกดปุ่มหยุด
    if stop_btn:
        ser.close()
        st.sidebar.warning("หยุดการทำงานแล้ว")
else:
    st.markdown(f"**ไม่พบอุปกรณ์ Arduino ที่พอร์ต {COM_PORT}**")

