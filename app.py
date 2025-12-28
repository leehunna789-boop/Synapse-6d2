import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests, geocoder
import pandas as pd
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
# ตรวจสอบ API Key จาก Streamlit Secrets เพื่อความปลอดภัย
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ใช้ชื่อรุ่นที่ถูกต้องเพื่อแก้ปัญหา Error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ใน Secrets (กรุณาตั้งค่าในหน้า Settings > Secrets)")
    st.stop()

# โครงสร้างข้อมูล (Emotional Matrix Assets)
MATRIX_V1 = {"JOY": {"F0": 0.8, "Vib": 0.9}, "SAD": {"F0": 0.3, "Vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3}
}

# --- 2. REAL-WORLD DATA ENGINE (ดึงข้อมูลจริง) ---
def get_live_environment():
    try:
        # ใช้ geocoder ดึงตำแหน่งจาก IP
        g = geocoder.ip('me') 
        lat, lon = g.latlng
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        res = requests.get(url).json()
        curr = res['current_weather']
        return {
            "weather": "Rainy" if curr['weathercode'] >= 51 else "Sunny",
            "temp": curr['temperature'],
            "city": g.city if g.city else "Current Location"
        }
    except:
        # ค่า Default กรณีดึงข้อมูลไม่ได้
        return {"weather": "Sunny", "temp": 25.0, "city": "Unknown Location"}

# --- 3. SYNAPSE ENGINE (BIO-FEEDBACK LOGIC) ---
class SynapseEngine:
    def lerp(self, low, high, factor): return low + (high - low) * factor

    def synthesize_resonance(self, v, bpm, weather):
        sr, duration = 44100, 5
        t = np.linspace(0, duration, sr * duration)
        
        # ปรับความถี่ตามชีพจรจริง (Bio-Feedback)
        pulse_mod = 75.0 / bpm 
        f0 = self.lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v) * pulse_mod
        vib = self.lerp(MATRIX_V1["SAD"]["Vib"], MATRIX_V1["JOY"]["Vib"], v)
        
        base = 0.5 * np.sin(2 * np.pi * (432 * f0) * t + (vib * 8 * np.sin(2 * np.pi * 5 * t)))
        if weather == "Rainy":
            base += np.random.normal(0, 0.04, len(t))
            
        audio_out = (np.clip(base * 0.7, -0.9, 0.9) * 32767).astype(np.int16)
        byte_io = io.BytesIO()
        wavfile.write(byte_io, sr, audio_out)
        return byte_io.getvalue()

# --- 4. UI/UX DESIGN ---
st.set_page_config(page_title="SYNAPSE Core V3.1", layout="wide")
st.markdown("<style>.stApp { background: #000428; color: white; }</style>", unsafe_allow_html=True)

st.title("💠 SYNAPSE CORE V3.1")
st.markdown(f"*\"อยู่นิ่งๆ ไม่เจ็บตัว - ระบบจัดการทุกอย่างด้วยข้อมูลจริง\"*")

# SIDEBAR: ข้อมูลจาก Sensor จริง
env = get_live_environment()
st.sidebar.header("📡 Live Sensor Data")
st.sidebar.info(f"📍 {env['city']} | 🌡️ {env['temp']}°C")
st.sidebar.write(f"สภาพอากาศจริง: **{env['weather']}**")
bpm = st.sidebar.slider("💓 Heart Rate (BPM)", 40, 160, 75)

user_input = st.text_area("ป้อนสภาวะภายในของคุณ...", placeholder="วันนี้รู้สึกอย่างไร...", height=100)

engine = SynapseEngine()

if st.button("🚀 ACTIVATE MATRIX SYNC"):
    if user_input:
        try:
            with st.status("🔮 กำลังซิงค์ข้อมูลจริงและ AI Matrix...", expanded=True) as status:
                # 1. AI Analysis
                prompt = f"Analyze the emotional valence of: '{user_input}'. Current weather is {env['weather']}. Return ONLY a JSON object: {{'v': 0.0-1.0}}"
                res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                v = json.loads(res.text).get('v', 0.5)
                
                # 2. V2.0 Visual Mapping
                vis = {k: engine.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v) for k in MATRIX_V2["JOY"]}
                
                # 3. Bio-Audio Synthesis
                audio_bytes = engine.synthesize_resonance(v, bpm, env['weather'])
                status.update(label="✅ Matrix Fully Synchronized!", state="complete")

            # --- DISPLAY DASHBOARD ---
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Emotional Matrix")
                st.metric("Valence (ความสุข)", f"{v*100:.1f}%")
                st.line_chart(pd.DataFrame({"Waveform": np.frombuffer(audio_bytes, dtype=np.int16)[:1000]}))
                st.audio(audio_bytes, format='audio/wav')

            with col2:
                st.subheader("🎨 Visual Output")
                for p, val in vis.items():
                    st.write(f"**{p}**")
                    st.progress(val)

            if bpm > 100:
                st.warning("⚠️ ชีพจรสูง: ระบบปรับความถี่ Resonance เพื่อช่วยให้คุณสงบ")
            st.balloons()
        except Exception as e:
            st.error(f"ระบบขัดข้อง: {e}")
