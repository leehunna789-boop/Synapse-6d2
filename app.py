import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import io
import os
import time
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
# ใช้ระบบ Secrets เพื่อดึงกุญแจ API อย่างปลอดภัย
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        # ใช้ชื่อรุ่นมาตรฐาน 'gemini-1.5-flash' เพื่อป้องกัน Error 404 Not Found
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("❌ ไม่พบ GEMINI_API_KEY ในระบบ Secrets ของ Streamlit")
        st.stop()
except Exception as e:
    st.error(f"⚠️ การเชื่อมต่อ AI ขัดข้อง: {e}")
    st.stop()

# --- 2. IP ASSET MATRIX (CORE LOGIC) ---
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "F0": 0.8, "Vib": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "F0": 0.3, "Vib": 0.2}
}

class SynapseEngine:
    def lerp(self, low, high, factor): 
        return low + (high - low) * factor

    def synthesize_audio(self, v, weather):
        sr = 44100
        duration = 6
        t = np.linspace(0, duration, sr * duration)
        f0 = self.lerp(MATRIX_V2["SAD"]["F0"], MATRIX_V2["JOY"]["F0"], v)
        vib = self.lerp(MATRIX_V2["SAD"]["Vib"], MATRIX_V2["JOY"]["Vib"], v)
        
        base = 0.5 * np.sin(2 * np.pi * (432 * f0) * t + (vib * 8 * np.sin(2 * np.pi * 5 * t)))
        noise = np.random.normal(0, 0.04, len(t))
        if weather == "Rainy": 
            noise = np.convolve(noise, np.ones(100)/100, mode='same') * (1.5 - v)
            
        combined = (base + noise) * 0.7
        env = np.ones_like(t)
        fade = sr // 2
        env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
        
        audio_out = (np.clip(combined * env, -0.9, 0.9) * 32767).astype(np.int16)
        byte_io = io.BytesIO()
        wavfile.write(byte_io, sr, audio_out)
        return byte_io.getvalue()

# --- 3. UI/UX DESIGN ---
st.set_page_config(page_title="SYNAPSE Matrix Engine", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001f3f 0%, #000428 100%); color: #e0e0e0; }
    .main-header { text-align: center; font-size: 60px; font-weight: 900; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .matrix-display { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 210, 255, 0.3); padding: 25px; border-radius: 20px; backdrop-filter: blur(10px); }
    .stButton>button { width: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff0055, #ff00ff); color: white; font-weight: bold; border: none; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. APP INTERFACE ---
# แสดงโลโก้เฉพาะเมื่อมีไฟล์ชื่อ logo.jpg ใน GitHub เท่านั้น
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.markdown("<div class='main-header'>SYNAPSE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00d2ff; letter-spacing:2px;'>GLOBAL ENERGY MATRIX</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

user_input = st.text_area("ป้อนสภาวะภายในของคุณเพื่อทำ Mapping...", placeholder="เช่น วันนี้อยากสงบ...", height=100)

engine = SynapseEngine()

if st.button("🚀 ACTIVATE MATRIX MAPPING"):
    if user_input:
        try:
            with st.status("📡 กำลังประมวลผล Matrix Intelligence...", expanded=True) as status:
                prompt = f"Analyze input: '{user_input}'. Return ONLY JSON: {{'v': float(0-1), 'a': float(0-1), 'weather': 'Rainy/Sunny/Night', 'chords': 'string'}}"
                res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                
                data = json.loads(res.text)
                v = data.get('v', 0.5)
                
                vis = {k: engine.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v) for k in ["SAT", "LIGHT", "CON"]}
                audio_bytes = engine.synthesize_audio(v, data.get('weather', 'Sunny'))
                
                status.update(label="✅ Matrix Synced สำเร็จ", state="complete")

            st.markdown("<div class='matrix-display'>", unsafe_allow_html=True)
            st.write("### 💎 Matrix Intelligence Dashboard")
            col1, col2, col3 = st.columns(3)
            col1.metric("Valence (อารมณ์)", f"{v*100:.1f}%")
            col2.metric("Energy (พลังงาน)", f"{data.get('a', 0.5)*100:.1f}%")
            col3.metric("Weather Context", data.get('weather'))

            st.write("#### Visual Control Matrix")
            v_col1, v_col2, v_col3 = st.columns(3)
            v_col1.metric("Saturation", f"{vis['SAT']:.2f}")
            v_col2.metric("Brightness", f"{vis['LIGHT']:.2f}")
            v_col3.metric("Contrast", f"{vis['CON']:.2f}")
            
            st.audio(audio_bytes, format='audio/wav')
            st.info(f"🔊 Resonance Sync: 432Hz | Chords: {data.get('chords', 'N/A')}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.balloons()

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณาป้อนข้อมูลก่อนทำการ Mapping")
