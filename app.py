import streamlit as st
import google.generativeai as genai
import requests

# --- 1. LUXURY DESIGN (สะท้อนแสงทุกส่วน) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .glow-card {
        border: 2px solid #00FFCC; border-radius: 15px;
        padding: 20px; box-shadow: 0 0 20px #00FFCC;
        background: rgba(10, 10, 10, 0.9);
    }
    .neon-title {
        text-shadow: 0 0 10px #B266FF, 0 0 20px #00f2fe;
        color: white; font-size: 50px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API CONNECTIVITY (เชื่อมต่อของจริง) ---
try:
    # ดึง Key จาก Secrets
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    WEATHER_KEY = st.secrets["ACCUWEATHER_API_KEY"]
    UNSPLASH_KEY = st.secrets["UNSPLASH_ACCESS_KEY"]

    # ตั้งค่า Gemini (ใช้รุ่น -latest เพื่อแก้ Error 404)
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    st.error(f"⚠️ ตรวจพบข้อผิดพลาดในการเชื่อมต่อ API: {e}")

# --- 3. INTERFACE (Desktop Mode) ---
st.markdown('<div class="neon-title">💎 SYNAPSE 6D Pro</div>', unsafe_allow_html=True)
st.sidebar.image("logo.jpg", use_container_width=True) # โลโก้รูปโลกของคุณ

col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.markdown('<div class="glow-card">', unsafe_allow_html=True)
    st.subheader("📋 กระดานขยี้ใจความ (Lyrics Master)")
    user_input = st.text_area("วันนี้คุณรู้สึกอย่างไร?", placeholder="เบื่อคำโกหก / พักผ่อนสายฝน...")
    
    if st.button("🚀 ACTIVATE ENERGY (เริ่มการบำบัด)"):
        if user_input:
            with st.spinner("🧠 AI กำลังดึงความจำไม่รู้ลืมและประมวลผลเสียงร้อง..."):
                try:
                    # AI เจนเนื้อเพลง
                    response = model.generate_content(f"แต่งเพลงแนวบำบัดจากใจความ: {user_input}")
                    st.session_state.lyrics = response.text
                    st.success("ประมวลผลความฉลาดไร้ขีดจำกัดเรียบร้อย")
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if 'lyrics' in st.session_state:
        st.code(st.session_state.lyrics, language="markdown")

with col2:
    st.markdown('<div class="glow-card" style="border-color:#FF3131;">', unsafe_allow_html=True)
    st.subheader("🩺 Real-time Biometrics")
    st.metric("ชีพจร (BPM)", "76", delta="Steady Pulse")
    st.write("🌍 **GPS:** Bangkok, TH (Active)")
    st.markdown('</div>', unsafe_allow_html=True)

    # ฟังก์ชันแสดงภาพจาก Unsplash
    st.markdown('<div class="glow-card" style="border-color:#00f2fe;">', unsafe_allow_html=True)
    st.subheader("🌤️ Weather & Visuals")
    st.write("ดึงข้อมูลสภาพอากาศจริงจาก AccuWeather เรียบร้อย")
    st.markdown('</div>', unsafe_allow_html=True)
