import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests, geocoder
import pandas as pd
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # จุดสำคัญ: ต้องระบุชื่อเต็มเป็น 'models/gemini-1.5-flash'
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ใน Secrets")
    st.stop()

# IP ASSET STRUCTURE
MATRIX_V1 = {"JOY": {"F0": 0.8, "Vib": 0.9}, "SAD": {"F0": 0.3, "Vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3}
}

# --- 2. REAL-WORLD DATA ENGINE ---
def get_live_environment():
    try:
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
        return {"weather": "Sunny", "temp": 25.0, "city": "Unknown"}

# --- 3. SYNAPSE ENGINE ---
class SynapseEngine:
    def lerp(self, low, high, factor): return low + (high - low) * factor
    def synthesize_resonance(self, v, bpm, weather):
        sr, duration = 44100, 5
        t = np.linspace(0, duration, sr * duration)
        pulse_mod = 75.0 / bpm 
        f0 = self.lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v) * pulse_mod
        vib = self.lerp(MATRIX_V1["SAD"]["Vib"], MATRIX_V1["JOY"]["Vib"], v)
        base = 0.5 * np.sin(2 * np.pi * (432 * f0) * t + (vib * 8 * np.sin(2 * np.pi * 5 * t)))
        if weather == "Rainy": base += np.random.normal(0, 0.04, len(t))
        audio_out = (np.clip(base * 0.7, -0.9, 0.9) * 32767).astype(np.int16)
        byte_io = io.BytesIO()
        wavfile.write(byte_io, sr, audio_out)
        return byte_io.getvalue()

# --- 4. UI DESIGN ---
st.set_page_config(page_title="SYNAPSE CORE V3.1", layout="wide")
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.title("💠 SYNAPSE CORE V3.1")
st.markdown("*\"อยู่นิ่งๆ ไม่เจ็บตัว - ระบบข้อมูลจริง\"*")

env = get_live_environment()
st.sidebar.header("📡 Live Sensor Data")
st.sidebar.info(f"📍 {env['city']} | 🌡️ {env['temp']}°C")
bpm = st.sidebar.slider("💓 ชีพจร (BPM)", 40, 160, 75)

user_input = st.text_area("ป้อนสภาวะภายในของคุณ...", height=100)
engine = SynapseEngine()

if st.button("🚀 ACTIVATE MATRIX SYNC"):
    if user_input:
        try:
            with st.status("🔮 กำลังประมวลผลข้อมูลจริง...", expanded=True) as status:
                prompt = f"Analyze: '{user_input}'. Return ONLY JSON: {{'v': 0.5}}"
                res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                v = json.loads(res.text).get('v', 0.5)
                audio_bytes = engine.synthesize_resonance(v, bpm, env['weather'])
                status.update(label="✅ Matrix Synced!", state="complete")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Valence (ความสุข)", f"{v*100:.1f}%")
                st.audio(audio_bytes, format='audio/wav')
            with col2:
                st.write("### Visual Matrix")
                st.progress(v)
            st.balloons()
        except Exception as e:
            st.error(f"ระบบขัดข้อง: {e}")
