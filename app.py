import streamlit as st
import numpy as np
import time
import os

# --- 1. การตั้งค่าหน้าจอและสไตล์พรีเมียม ---
st.set_page_config(page_title="SYNAPSE 6D ENERGY PRO", page_icon="💎", layout="centered")

# ปรับแต่งธีมแอปให้ดูหรูหราและสมจริง
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050531 50%, #020111 100%); color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(90deg, #ff0000, #ff416c); color: white; 
        border-radius: 30px; border: none; width: 100%; height: 4em; font-weight: bold; font-size: 20px;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ระบบเลือกดนตรีสมจริง (Sound Engine) ---
def get_therapy(user_text):
    text = user_text.lower()
    if any(word in text for word in ['เหนื่อย', 'เครียด', 'เศร้า']):
        return {
            "title": "Deep Healing Piano (เสียงเปียโนสมจริง)",
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
            "video": "https://www.youtube.com/watch?v=668nUCeB4bw"
        }
    else:
        return {
            "title": "Nature Energy (เสียงธรรมชาติสมจริง)",
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
            "video": "https://www.youtube.com/watch?v=nMfPqeZjc2c"
        }

# --- 3. แสดงผลโลโก้และสโลแกน ---
logo_path = "logo.jpg"
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True)

st.markdown("<h3 style='text-align: center; color: #ff4b2b;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</h3>", unsafe_allow_html=True)

# --- 4. ฟังก์ชันพิเศษ: Zen Energy Charge ---
st.write("---")
if st.toggle("🧘‍♂️ เปิดระบบชาร์จพลังความนิ่ง"):
    st.info("กรุณานิ่ง... ระบบกำลังซิงค์พลังงาน 6D")
    bar = st.progress(0)
    for p in range(101):
        time.sleep(0.03)
        bar.progress(p)
    st.success("✨ ชาร์จพลังงานสำเร็จ! 'อยู่นิ่งๆ ไม่เจ็บตัว' ของจริง")

# --- 5. ระบบบำบัดด้วยเสียงและภาพสมจริง ---
st.write("---")
user_feeling = st.text_area("สภาวะจิตใจของคุณ:", placeholder="ระบุความรู้สึกที่นี่...")

if st.button("🔥 ACTIVATE 6D REALISTIC THERAPY"):
    if user_feeling:
        therapy = get_therapy(user_feeling)
        with st.status("⚡ กำลังเตรียมกระบวนการบำบัดสมจริง...", expanded=True):
            time.sleep(1.5)
            st.write(f"🎵 จูนเสียงดนตรี: {therapy['title']}")
            time.sleep(1)
        
        st.balloons()
        st.subheader(f"🔊 กำลังเล่น: {therapy['title']}")
        st.audio(therapy['audio']) # เสียงดนตรีจริง
        
        st.write("---")
        st.subheader("📺 Visual Therapy (4K)")
        st.video(therapy['video']) # วิดีโอวิวธรรมชาติสมจริง
        
        st.success(f"ระบบบำบัดสำหรับ '{user_feeling}' พร้อมแล้ว... นิ่งเข้าไว้นะครับ")
    else:
        st.warning("กรุณาระบุความรู้สึกก่อน")

# --- 6. ส่วนท้าย ---
st.markdown("---")
st.caption("🔵🔴⚪ SYNAPSE 6D HIGH-PERFORMANCE SYSTEM")
