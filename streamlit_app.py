import streamlit as st
import numpy as np

# 1. ตั้งค่า Page ให้เป็นสไตล์ Industrial
st.set_page_config(page_title="SYNAPSE CORE", layout="wide")

# 2. Custom CSS: ความจริงที่ไม่มีความหวานแหวว
st.markdown("""
    <style>
    .reportview-container, .main { background: #000000; color: #00FF00; font-family: 'Courier New', Courier, monospace; }
    .stProgress > div > div > div > div { background-color: #00FF00; }
    h1, h2, h3 { color: #FFFFFF; border-bottom: 1px solid #333; }
    .status-box { border: 1px solid #00FF00; padding: 10px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_status_code=True)

st.title("SYNAPSE CORE v1.0")

# ส่วนบน: Status Bar
col1, col2 = st.columns([3, 1])
with col1:
    st.text("ID: SSS-MUSIC-MATRIX-001")
with col2:
    st.markdown('<div class="status-box">STATUS: EXECUTE</div>', unsafe_allow_status_code=True)

st.write("---")

# ส่วนกลาง: ข้อมูลจาก "แขน" Logic
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("RAW DATA")
    freq_val = st.empty()
    vol_val = st.empty()
    st.progress(65) # ตัวอย่างการแสดงผลแถบพลัง

with col_b:
    st.subheader("CONTROL MATRIX")
    # ตัวอย่างการจำลองจุด Vector ที่ขยับตามเสียง
    st.code("""
    VECTOR_X: 0.452
    VECTOR_Y: 0.128
    VECTOR_Z: 0.889
    STATE: SYNCING...
    """)

st.write("---")

# ส่วนล่าง: ปรัชญาของคุณ
st.markdown("### >> SLOGAN: **อยู่นิ่งๆ ไม่เจ็บตัว**")

# Logic จำลองการ Update หน้าจอ (Real-time Simulation)
import time
if st.button("RUN SYSTEM"):
    for i in range(100):
        fake_freq = 440 + np.random.uniform(-5, 5)
        freq_val.text(f"FREQUENCY: {fake_freq:.2f} Hz")
        vol_val.text(f"AMPLITUDE: {np.random.random():.3f}")
        time.sleep(0.1)
