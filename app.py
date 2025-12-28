import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests, geocoder
import pandas as pd
from scipy.io import wavfile

# --- 1. CONFIGURATION & DESIGN (ม่วง-ดำ-เขียวมินต์) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; } 
    h1, h2, h3 { color: #B266FF !important; text-shadow: 2px 2px 4px #000000; }
    .stMetric { background-color: #1E1E1E; border-radius: 10px; padding: 15px; border: 1px solid #B266FF; }
    .stButton>button { 
        background-color: #00CC99; 
        color: white; border-radius: 25px; width: 100%; font-weight: bold; height: 50px;
        box-shadow: 0px 4px 15px rgba(0, 204, 153, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CORE (ดึงกุญแจจากหน้า Secrets) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ระบุชื่อรุ่นให้ถูกต้องเพื่อแก้ Error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ในหน้า Secrets")
    st.info("กรุณาตรวจสอบว่าในหน้า Settings > Secrets ใส่ GEMINI_API_KEY = 'รหัสของคุณ' แล้ว")
    st.stop()

# --- 3. IP ASSET MATRIX (Vocal V1.0 & Visual V2.0) ---
MATRIX_V1 = {"JOY": {"f0": 0.8, "vib": 0.9}, "SAD": {"f0": 0.3, "vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3}
}

class SynapseSystem:
    def synthesize_sound(self, v):
        sr = 44100
        t = np.linspace(0, 5, sr * 5)
        # ปรับความถี่คลื่นตาม Valence (v) และอิงฐาน 432Hz
        wave = 0.4 * np.sin(2 * np.pi * (432 * (0.5 + v)) * t) 
        envelope = np.ones_like(t)
        fade = sr // 2
        envelope[:fade] = np.linspace(0, 1, fade)
        envelope[-fade:] = np.linspace(1, 0, fade)
        return (np.clip(wave * envelope, -0.9, 0.9) * 32767).astype(np.int16)

# --- 4. UI/UX INTERFACE ---
# แสดงโลโก้
if os.path.exists("1000008885.jpg"):
    st.image("1000008885.jpg", use_container_width=True)

st.title("💎 SYNAPSE : 6D ENERGY PRO")
st.subheader("ระบบปรับจูนพลังงานระดับเซลล์ของคุณ")

sys = SynapseSystem()
user_input = st.text_area("บอกความรู้สึกของคุณวันนี้ให้ระบบรับรู้:", placeholder="เบื่อ / เหนื่อย / ต้องการพลังงาน...")

if st.button("🚀 ACTIVATE ENERGY"):
    if user_input:
        with st.spinner("🔮 ระบบกำลังดึงกุญแจจริงจาก Secrets และประมวลผล Matrix..."):
            try:
                # AI Analysis
                prompt = f"Analyze emotion: '{user_input}'. Return ONLY JSON: {{'v': 0.0-1.0, 'a': 0.0-1.0, 'chords': 'string'}}"
                res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                data = json.loads(res.text)
                
                audio = sys.synthesize_sound(data['v'])
                
                st.subheader(f"🎨 สภาวะพลังงาน (Valence: {data['v']*100:.1f}%)")
                c1, c2 = st.columns(2)
                c1.metric("ความสว่างเซลล์ (Light)", f"{data['v']*100:.1f}%")
                c2.metric("ความเข้มข้น (Contrast)", f"{data['a']*100:.1f}%")

                st.audio(audio, format='audio/wav', sample_rate=44100)
                st.success("✅ ปรับจูนพลังงานเรียบร้อยด้วยกุญแจจริงของคุณ")
                st.info("สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว' - ทุกอย่างซิงค์กับ Secrets แล้ว")
                st.balloons()
            except Exception as e:
                st.error(f"ระบบขัดข้อง: {e}")
    else:
        st.error("กรุณากรอกความรู้สึกก่อนครับ")
