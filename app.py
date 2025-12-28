import streamlit as st
import time
import os

# --- 1. ตั้งค่าหน้าจอและสไตล์ ---
st.set_page_config(
    page_title="SYNAPSE 6D ENERGY PRO",
    page_icon="💎",
    layout="centered"
)

# ปรับแต่งธีมแอป (สีน้ำเงิน-แดง ตามสไตล์ SYNAPSE)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF4B2B, #FF416C);
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
        height: 3.5em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. แสดงโลโก้ (ไฟล์ชื่อ logo.jpg ที่คุณเตรียมไว้) ---
logo_file = "logo.jpg" 

if os.path.exists(logo_file):
    st.image(logo_file, use_container_width=True)
else:
    st.markdown("<h1 style='text-align: center;'>💎 SYNAPSE 6D</h1>", unsafe_allow_html=True)

# --- 3. สโลแกนประจำตัว ---
st.markdown("<h3 style='text-align: center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</h3>", unsafe_allow_html=True)
st.write("---")

# --- 4. ฟังก์ชันบำบัดด้วยความนิ่ง (Zen Mode) ---
st.subheader("🧘‍♂️ ระบบบำบัดด้วยความนิ่ง")
if st.toggle("เปิดใช้งานโหมดชาร์จพลัง"):
    st.info("กรุณานิ่ง... ระบบกำลังซิงค์พลังงาน 6D")
    progress_bar = st.progress(0)
    for i in range(101):
        time.sleep(0.04)
        progress_bar.progress(i)
    st.success("✅ ชาร์จพลังงานสำเร็จ! 'อยู่นิ่งๆ ไม่เจ็บตัว' ของจริง")

# --- 5. ส่วนรับข้อมูลและปุ่ม ACTIVATE ---
st.write("---")
user_input = st.text_input("ระบุอาการของคุณ:", placeholder="เช่น เหนื่อยล้า")

if st.button("🔥 ACTIVATE 6D ENERGY"):
    if user_input:
        with st.status("⚡ กำลังประมวลผล...", expanded=True):
            time.sleep(2)
        st.balloons()
        st.success(f"ส่งพลังงานสำหรับ '{user_input}' เรียบร้อย... อยู่นิ่งๆ นะครับ")
    else:
        st.warning("กรุณากรอกข้อความก่อน")
