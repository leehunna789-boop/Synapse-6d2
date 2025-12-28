import streamlit as st
import time
import os

# --- 1. ตั้งค่าหน้าตาแอปและธีมสี (สไตล์ SYNAPSE) ---
st.set_page_config(
    page_title="SYNAPSE 6D ENERGY PRO",
    page_icon="💎",
    layout="centered"
)

# ปรับแต่ง CSS เพื่อให้พื้นหลังและปุ่มดูแพง (Gradient Design)
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
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px #FF416C;
    }
    </style>
    """, unsafe_allow_config=True)

# --- 2. การแสดงผลโลโก้ (ตั้งชื่อไฟล์ให้จำง่าย) ---
# สำคัญ: คุณต้องอัปโหลดรูปขึ้น GitHub และตั้งชื่อไฟล์ว่า logo.jpg
logo_filename = "logo.jpg" 

if os.path.exists(logo_filename):
    st.image(logo_filename, use_container_width=True)
else:
    # แสดงหัวข้อสำรองถ้ายังไม่ได้อัปโหลดรูป
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💎 SYNAPSE 6D ENERGY</h1>", unsafe_allow_config=True)

# --- 3. สโลแกนประจำตัว ---
st.markdown("<h3 style='text-align: center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</h3>", unsafe_allow_config=True)
st.write("---")

# --- 4. ฟังก์ชันแปลกใหม่: Zen Energy Healing ---
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
user_input = st.text_input("ระบุอาการหรือความเหนื่อยล้าของคุณ:", placeholder="เช่น เหนื่อยล้า")

if st.button("🔥 ACTIVATE 6D ENERGY"):
    if user_input:
        with st.status("⚡ กำลังประมวลผลคลื่น SYNAPSE...", expanded=True) as status:
            st.write("🔍 วิเคราะห์สภาวะจิตใจ...")
            time.sleep(1)
            st.write("🔄 ปรับคลื่น Sound & Visual Therapy...")
            time.sleep(1.2)
            status.update(label="การบำบัดเสร็จสิ้น!", state="complete")
        
        st.balloons() # เอฟเฟกต์ลูกโป่ง
        st.snow()     # เอฟเฟกต์หิมะ
        st.success(f"ส่งพลังงานบำบัดสำหรับ '{user_input}' ให้คุณแล้ว... ตอนนี้นิ่งเข้าไว้ครับ")
    else:
        st.warning("กรุณากรอกข้อความก่อนเริ่มระบบ")

# --- 6. ส่วนท้าย (Footer) ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>🔵🔴⚪ SYNAPSE 6D HIGH-PERFORMANCE SYSTEM<br>STAY STILL & HEAL</p>", unsafe_allow_config=True)
