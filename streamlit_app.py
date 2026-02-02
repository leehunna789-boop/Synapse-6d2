import streamlit as st
import google.generativeai as genai
import numpy as np
import pandas as pd
import json
import time
import random

# --- [ 1. CONFIGURATION & THEME ] ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Kanit', sans-serif; }
    .neon-title { 
        color: #FF0000; 
        text-shadow: 0 0 20px #FF0000, 0 0 30px #FF0000; 
        font-size: 70px; text-align: center; font-weight: 900; margin-bottom: 0px;
    }
    .slogan { color: #00FF00; text-align: center; font-size: 20px; text-shadow: 0 0 10px #00FF00; margin-top: -10px; }
    
    /* ไฟกระพริบสถานะ */
    .status-flash {
        padding: 10px; border-radius: 10px; text-align: center; font-weight: bold;
        animation: blinker 0.8s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.3; } }
    
    .luxury-card {
        background: rgba(20, 20, 20, 0.95);
        border: 2px solid #00F2FE;
        border-radius: 20px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 242, 254, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- [ 2. API & LOGIC ENGINE ] ---
try:
    # ดึง Key จาก Secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ กรุณาตั้งค่า GEMINI_API_KEY ใน Secrets")
    model = None

def get_synapse_logic():
    """6-Logic Integration: ดึงค่าจำลองจากเซนเซอร์"""
    bpm = np.random.randint(65, 85)
    temp = round(np.random.uniform(32.0, 36.5), 1)
    # Healing Logic: เลือกความถี่บำบัด
    freq = 432 if bpm < 80 else 528
    return bpm, temp, freq

# --- [ 3. HEADER & LOGO ] ---
st.markdown('<p class="neon-title">SYNAPSE 6D</p>', unsafe_allow_html=True)
st.markdown('<p class="slogan">SOUND & VISUAL THERAPY | อยู่นิ่งๆ ไม่เจ็บตัว</p>', unsafe_allow_html=True)

# --- [ 4. DASHBOARD: BIO-LOGIC & ATMOS-LOGIC ] ---
bpm, temp, freq = get_synapse_logic()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="luxury-card"><h4 style="color:#FF0000;">❤️ Pulse (Bio)</h4><h2 style="color:white;">{bpm} BPM</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="luxury-card"><h4 style="color:#00FF00;">🌡️ Temp (Atmos)</h4><h2 style="color:white;">{temp} °C</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="luxury-card"><h4 style="color:#00F2FE;">Hz Healing</h4><h2 style="color:white;">{freq} Hz</h2></div>', unsafe_allow_html=True)

# --- [ 5. AI MUSIC GENERATOR (Linguistic & Integration) ] ---
st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
st.subheader("📝 ระบายอารมณ์เพื่อสร้างบทเพลงบำบัด")
user_msg = st.text_area("ตอนนี้รู้สึกยังไง... บอกช่างใหญ่ AI หน่อย", placeholder="พิมพ์ความรู้สึกที่นี่...")

if st.button("RUN INTEGRATION LOGIC"):
    if user_msg and model:
        with st.spinner('กำลังประมวลผลโลจิกทั้ง 6 ชุด...'):
            prompt = f"""
            คุณคือ AI โปรดิวเซอร์ระดับโลก แต่งเพลงไทยบำบัดจาก: "{user_msg}"
            Bio-Data: {bpm} BPM, {temp}C, {freq}Hz
            ตอบเป็น JSON เท่านั้น: 
            {{ "title": "ชื่อเพลง", "genre": "แนวเพลง", "lyrics": "เนื้อเพลงสั้นๆ 4 บรรทัด", "advice": "คำแนะนำการใช้ชีวิต" }}
            """
            try:
                response = model.generate_content(prompt)
                res_data = json.loads(response.text.replace('```json', '').replace('```', ''))
                
                st.success(f"🎵 {res_data['title']}")
                st.info(f"แนวเพลง: {res_data['genre']}")
                st.write(res_data['lyrics'])
                st.warning(f"💡 คำแนะนำ: {res_data['advice']}")
                st.balloons()
            except:
                st.write("AI กำลังจูนคลื่น... ลองส่งข้อความใหม่อีกครั้ง")
    else:
        st.warning("กรุณาใส่ข้อความหรือตรวจสอบ API Key")
st.markdown('</div>', unsafe_allow_html=True)

# --- [ 6. VISUAL LOGIC & MULTIMEDIA ] ---
st.write("---")
st.markdown("<div class='status-flash' style='background-color:#FF0000; color:white;'>🔴 LIVE SYNC: ON AIR</div>", unsafe_allow_html=True)

v_col1, v_col2 = st.columns(2)
with v_col1:
    st.markdown("### 📽️ 4K Visual Therapy")
    # ตัวอย่างวิดีโอผ่อนคลาย
    st.video("https://www.youtube.com/watch?v=n61ULEU7CO0")

with v_col2:
    st.markdown("### 🎼 6D Audio Layer")
    # โหลดวิดีโอเพลงที่สองเพื่อสร้าง Layer เสียง
    st.video("https://www.youtube.com/watch?v=cbcuYnyr828")

# --- [ 7. EXTRA YOUTUBE (5 ช่องตามคำขอ) ] ---
st.write("---")
st.markdown("### 🎵 Additional Healing Channels")
yt_links = [
    "https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO",
    "https://www.youtube.com/watch?v=Bb3Jtsik3nY",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=yK1lT73hI9g",
    "https://www.youtube.com/watch?v=5qap5aO4i9A"
]

yt_tabs = st.tabs(["CH 1", "CH 2", "CH 3", "CH 4", "CH 5"])
for i, tab in enumerate(yt_tabs):
    with tab:
        st.video(yt_links[i])

# --- [ 8. UPLOAD & SOCIAL ] ---
st.write("---")
u_col1, u_col2 = st.columns(2)
with u_col1:
    st.file_uploader("📸 อัปโหลดรูปภาพบำบัด", type=["jpg", "png"])
with u_col2:
    st.file_uploader("🎥 อัปโหลดวิดีโอส่วนตัว", type=["mp4"])

st.link_button("🔵 แชร์ความรู้สึกไปยัง Facebook", "https://www.facebook.com")
st.link_button("🟢 แชทกับดีเจบอล (LINE)", "https://line.me")

# Sidebar
st.sidebar.image("https://via.placeholder.com/150", caption="DJ บอล ON AIR")
st.sidebar.markdown(f"**สถานะระบบ:** 🟢 ปกติ")
st.sidebar.markdown(f"**โลจิก:** 6-Logic Active")
st.sidebar.markdown(f"**ความถี่:** {freq} Hz")
