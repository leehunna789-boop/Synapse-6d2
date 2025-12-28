import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import io
import os
import time
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
# ใช้ API Key ที่คุณได้รับมาจริงเพื่อเปิดใช้งานสมองกลระดับสูง
API_KEY = "AIzaSyBiKFHClySIV_UmeMznANnhyBoD78CYUrg" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. IP ASSET MATRIX (V1.0 & V2.0 CORE LOGIC) ---
MATRIX_V1 = {"JOY": {"F0": 0.8, "Vib": 0.9}, "SAD": {"F0": 0.3, "Vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3}
}

class SynapseEngine:
    def lerp(self, low, high, factor): return low + (high - low) * factor

    def synthesize_advanced_audio(self, v, a, weather):
        sr = 44100
        duration = 10
        t = np.linspace(0, duration, sr * duration)
        f0 = self.lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v)
        vib = self.lerp(MATRIX_V1["SAD"]["Vib"], MATRIX_V1["JOY"]["Vib"], v)
        base = 0.5 * np.sin(2 * np.pi * (432 * f0) * t + (vib * 8 * np.sin(2 * np.pi * 5 * t)))
        harmony = 0.2 * np.sin(2 * np.pi * (432 * f0 * 1.5) * t)
        noise = np.random.normal(0, 0.05, len(t))
        if weather == "Rainy": noise = np.convolve(noise, np.ones(100)/100, mode='same') * (1.2 - v)
        combined = base + harmony + noise
        env = np.ones_like(t); fade = sr // 2; env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
        return (np.clip(combined * env, -0.9, 0.9) * 32767).astype(np.int16)

# --- 3. UI/UX DESIGN (High-End Professional) ---
st.set_page_config(page_title="SYNAPSE Matrix Engine", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001f3f 0%, #000428 100%); color: #e0e0e0; }
    .main-header { text-align: center; font-size: 70px; font-weight: 900; background: -webkit-linear-gradient(#ff0055, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0px 0px 30px rgba(255, 0, 85, 0.6); margin-bottom: 0px; }
    .sub-header { text-align: center; font-size: 20px; color: #00d2ff; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 40px; text-shadow: 0 0 10px #00d2ff; }
    .stButton>button { width: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff0055, #ff00ff); color: white; padding: 20px; font-size: 22px; font-weight: bold; box-shadow: 0 0 30px rgba(255, 0, 85, 0.5); border: none; transition: 0.5s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 60px rgba(255, 0, 85, 0.9); }
    .matrix-display { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 210, 255, 0.3); padding: 30px; border-radius: 25px; backdrop-filter: blur(15px); }
    </style>
""", unsafe_allow_html=True)

# --- 4. APP INTERFACE ---
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.markdown("<div class='main-header'>SYNAPSE</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Global Energy Matrix</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>\"พลังงานเพื่อโลก... อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

with st.expander("⚡ คาร์จพลังงานโลก (Zen Earth Charge Sync)"):
    if st.button("START GLOBAL SYNC"):
        bar = st.progress(0)
        for i in range(101): time.sleep(0.01); bar.progress(i)
        st.success("Syncing complete! ระบบพร้อมรับการบำบัด")

user_input = st.text_area("ป้อนสภาวะภายในของคุณ", placeholder="เช่น วันนี้เหนื่อยจัง แต่อยากสงบ...")

engine = SynapseEngine()

if st.button("🚀 ACTIVATE MATRIX MAPPING"):
    if user_input:
        with st.status("📡 กำลังงัดศักยภาพ AI และประมวลผล 3D Matrix...", expanded=True) as status:
            prompt = f"Analyze: '{user_input}'. Return ONLY JSON: {{'v': 0.0-1.0, 'a': 0.0-1.0, 'weather': 'Rainy/Sunny/Night', 'chords': 'string'}}"
            res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(res.text)
            v = data['v']
            vis = {k: engine.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v) for k in MATRIX_V2["JOY"]}
            audio = engine.synthesize_advanced_audio(v, data['a'], data['weather'])
            status.update(label="✅ การประมวลผล Matrix สำเร็จ", state="complete")

        st.markdown("<div class='matrix-display'>", unsafe_allow_html=True)
        st.write("### 💎 Matrix Intelligence Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Valence (อารมณ์)", f"{v*100:.1f}%")
        col2.metric("Arousal (พลังงาน)", f"{data['a']*100:.1f}%")
        col3.metric("Weather", data['weather'])

        st.write("#### Visual Control Matrix (V2.0)")
        v_col1, v_col2, v_col3 = st.columns(3)
        v_col1.metric("Saturation", f"{vis['SAT']:.2f}")
        v_col2.metric("Light", f"{vis['LIGHT']:.2f}")
        v_col3.metric("Contrast", f"{vis['CON']:.2f}")
        
        st.audio(audio, format='audio/wav', sample_rate=44100)
        st.info(f"🔊 Resonance: 432Hz | Chords: {data['chords']}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.balloons()
