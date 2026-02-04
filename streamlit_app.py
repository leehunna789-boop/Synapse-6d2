import streamlit as st
import serial
import serial.tools.list_ports
import time
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="ระบบวัดระดับเสียง", layout="wide")

# --- ฟังก์ชันช่วยเลือกพอร์ต ---
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

@st.cache_resource
def get_serial_connection(port, baudrate):
    try:
        # เพิ่ม dsrdtr=True หรือ rtscts=True หาก Arduino บางรุ่นรีเซ็ตตัวเองบ่อย
        ser = serial.Serial(port, baudrate, timeout=0.1) 
        return ser
    except Exception as e:
        return None

# --- UI Sidebar ---
st.sidebar.header("⚙️ การตั้งค่าอุปกรณ์")
available_ports = list_serial_ports()
selected_port = st.sidebar.selectbox("เลือก Serial Port", available_ports if available_ports else ["ไม่พบอุปกรณ์"])
baud_rate = st.sidebar.selectbox("Baud Rate", [9600, 115200], index=0)

run_system = st.sidebar.toggle("เริ่มการทำงานระบบ", value=False)

# --- พื้นที่แสดงผล ---
st.title("🔊 ระบบวัดระดับเสียงและความแม่นยำ")
col1, col2 = st.columns([1, 3])
metric_placeholder = col1.empty()
chart_placeholder = col2.empty()

# เตรียม State ข้อมูล
if 'history_data' not in st.session_state:
    st.session_state.history_data = pd.DataFrame(columns=['Time', 'Level'])

# --- ส่วนการทำงานหลัก ---
if run_system and selected_port != "ไม่พบอุปกรณ์":
    ser = get_serial_connection(selected_port, baud_rate)
    
    if ser:
        try:
            # ใช้ st.empty() เพื่อสร้างพื้นที่สำหรับปุ่มหยุด (ถ้าต้องการหยุดจากหน้าหลัก)
            while run_system:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    try:
                        value = float(line)
                        current_time = datetime.now().strftime("%H:%M:%S")

                        # อัปเดต Metric
                        metric_placeholder.metric(label="ระดับเสียงปัจจุบัน (dB)", value=f"{value:.2f}")

                        # อัปเดตข้อมูล (รักษาไว้แค่ 50 ค่าล่าสุด)
                        new_data = pd.DataFrame({'Time': [current_time], 'Level': [value]})
                        st.session_state.history_data = pd.concat([st.session_state.history_data, new_data], ignore_index=True).tail(50)
                        
                        # แสดงกราฟ
                        chart_placeholder.line_chart(st.session_state.history_data.set_index('Time'))
                        
                    except ValueError:
                        pass # ข้ามบรรทัดที่ข้อมูลไม่สมบูรณ์เพื่อไม่ให้ระบบ "เจ็บตัว"
                
                time.sleep(0.1) # ปรับความเร็วให้เหมาะสม ไม่ให้ CPU ทำงานหนักเกินไป
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
            st.session_state.history_data = pd.DataFrame(columns=['Time', 'Level']) # ล้างข้อมูลเก่ากรณีหลุด
    else:
        st.error("ไม่สามารถเปิดการเชื่อมต่อได้ ตรวจสอบว่ามีโปรแกรมอื่นใช้พอร์ตนี้อยู่หรือไม่")
else:
    st.info("กรุณาเลือกพอร์ตและกด 'เริ่มการทำงานระบบ' ที่แถบด้านซ้าย")
    # ปิดการเชื่อมต่อเมื่อ Toggle เป็น False
    if 'ser' in locals() and ser:
        ser.close()
