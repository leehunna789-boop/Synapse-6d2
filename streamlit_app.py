import streamlit as st
import serial
import serial.tools.list_ports
import time
import pandas as pd
from datetime import datetime

# --- การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="Sound Monitor Pro", layout="wide")

# --- ฟังก์ชันจัดการ Serial (หัวใจหลักของความเสถียร) ---
def get_all_ports():
    return [p.device for p in serial.tools.list_ports.comports()]

@st.cache_resource
def init_serial(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=0.1)
        return ser
    except:
        return None

# --- ส่วนของการจัดการ Session State ---
if 'db_history' not in st.session_state:
    st.session_state.db_history = pd.DataFrame(columns=['Timestamp', 'dB'])
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# --- Sidebar: ส่วนควบคุม ---
with st.sidebar:
    st.header("🛠 การตั้งค่า")
    ports = get_all_ports()
    target_port = st.selectbox("เลือก Port Arduino", ports if ports else ["ไม่พบอุปกรณ์"])
    baudrate = st.select_slider("Baudrate", options=[9600, 115200], value=9600)
    
    st.divider()
    
    # ปุ่มเริ่ม/หยุด (ใช้ Toggle เพื่อความนิ่ง)
    run_trigger = st.toggle("เริ่มการวัดค่า", value=st.session_state.is_running)
    st.session_state.is_running = run_trigger

    # ปรับจูนค่า (Calibration)
    offset = st.number_input("ค่าชดเชยเสียง (dB Offset)", value=0.0)
    
    if st.button("ล้างข้อมูลทั้งหมด"):
        st.session_state.db_history = pd.DataFrame(columns=['Timestamp', 'dB'])
        st.rerun()

# --- Main Page: แสดงผล ---
st.title("🔊 ระบบติดตามระดับเสียง Real-time")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("ค่าปัจจุบัน")
    metric_spot = st.empty()
    st.info("แนะนำ: ควรวางเซนเซอร์ห่างจากแหล่งกำเนิดเสียงประมาณ 1 เมตร")

with col2:
    st.subheader("กราฟแนวโน้ม")
    chart_spot = st.empty()

# --- Logic การอ่านค่า ---
if st.session_state.is_running and target_port != "ไม่พบอุปกรณ์":
    ser = init_serial(target_port, baudrate)
    
    if ser:
        try:
            # วนลูปอ่านค่า (Streamlit จะทำงานในลูปนี้จนกว่าจะกด Stop)
            while st.session_state.is_running:
                if ser.in_waiting > 0:
                    raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    try:
                        # แปลงค่าและใส่ Offset
                        val = float(raw_data) + offset
                        now = datetime.now().strftime("%H:%M:%S")

                        # อัปเดตข้อมูลใน Session
                        new_entry = pd.DataFrame({'Timestamp': [now], 'dB': [val]})
                        st.session_state.db_history = pd.concat([st.session_state.db_history, new_entry], ignore_index=True).tail(30)

                        # แสดงผลบน UI
                        metric_spot.metric("ระดับเสียง (dB)", f"{val:.1f} dB")
                        chart_spot.line_chart(st.session_state.db_history.set_index('Timestamp'))
                        
                    except ValueError:
                        continue # ข้ามข้อมูลที่อ่านไม่รู้เรื่อง
                
                time.sleep(0.05) # หน่วงเวลาเล็กน้อยเพื่อลดภาระ CPU
                
        except Exception as e:
            st.error(f"การเชื่อมต่อหลุด: {e}")
            st.session_state.is_running = False
    else:
        st.error("ไม่สามารถเชื่อมต่อกับ Arduino ได้ (อาจถูกโปรแกรมอื่นใช้งานอยู่)")
else:
    st.warning("กรุณาเลือก Port และกด 'เริ่มการวัดค่า'")

# --- ส่วนท้าย: ดาวน์โหลดข้อมูล ---
if not st.session_state.db_history.empty:
    st.divider()
    csv = st.session_state.db_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลเป็น CSV",
        data=csv,
        file_name=f"sound_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
    )
