import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import io
import os
import time
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
# ใช้ระบบ Secrets เพื่อไม่ต้องระบุ Key ในโค้ดโดยตรง (ปลอดภัยและสะดวกกว่า)
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        # กรณีรัน Local แล้วไม่ได้ตั้ง Secrets ให้ใส่ตรงนี้ชั่วคราวได้
        API_KEY = "ใส่_API_KEY_ของคุณที่นี่_ถ้าไม่ได้ใช้_Secrets"
    
    genai.configure(api_key=API_KEY)
    # ใช้รุ่นล่าสุด (Free Tier) ที่ฉลาดและเสถียรที่สุด
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("⚠️ ไม่พบ API Key: กรุณาตั้งค่าใน Streamlit Secrets")
    st.stop()

# --- 2. IP ASSET MATRIX (LOGIC V2.1) ---
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9, "F0": 0.8, "Vib": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3, "F0": 0.3, "Vib": 0.2}
}

class SynapseEngine:
    def lerp(self, low, high, factor): 
        return low + (high - low) * factor

    def synthesize_audio(self, v, a, weather):
        sr = 44100
        duration = 6  # ความยาวเสียง 6 วินาที
        t = np.linspace(0, duration, sr * duration)
        
        # ดึงค่าความถี่จากการประมวลผล Matrix
        f0_val = self.lerp(MATRIX_V2["SAD"]["F0"], MATRIX_V2["JOY"]["F0"], v)
        vib_val = self.lerp(MATRIX_V2["SAD"]["Vib"], MATRIX_V2["JOY"]["Vib"], v)
        
        # สร้างคลื่นเสียง Resonance 432Hz
        base = 0.5 * np.sin(2 * np.pi * (432 * f0_val) * t + (vib_val * 8 * np.sin(2 * np.pi * 5 * t)))
        noise = np.random.normal(0, 0.03, len(t))
        if weather == "Rainy": 
            noise = np.convolve(noise, np.ones(100)/100, mode='same') * (1.5 - v)
            
        combined = (base + noise) * 0.7
        env = np.ones_like(t)
        fade = sr // 2
        env[:fade] = np.linspace(0, 1, fade)
        env[-fade:] = np.linspace(1, 0, fade)
        
        audio_out = (np.clip(combined * env, -0.9, 0.9) * 32767).astype(np.int16)
        byte_io = io.BytesIO()
        wavfile.write(byte_io, sr, audio_out)
        return byte_io.getvalue()

# --- 3. UI/UX DESIGN ---
st.set_page_config(page_title="SYNAPSE Matrix", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #000428; background: radial-gradient(circle, #001f3f 0%, #000428 100%); color: white; }
    .main-header { text-align: center; font-size: 65px; font-weight: 900; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(90deg, #ff0055, #ff00ff); border: none; color: white; padding: 15px; font-weight: bold; font-size: 1.2rem; }
    .matrix-box { background: rgba(255, 255, 255, 0.07); padding: 25px; border-radius: 20px; border: 1px solid rgba(0, 210, 255, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- 4. APP INTERFACE ---
st.markdown("<div class='main-header'>SYNAPSE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: #00d2ff; letter-spacing: 3px;'>GLOBAL ENERGY MATRIX</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity: 0.8;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

user_text = st.text_area("ระบุสภาวะจิตใจของคุณตอนนี้...", placeholder="เช่น รู้สึกสงบเหมือนอยู่ท่ามกลางป่าฝน", height=120)

engine = SynapseEngine()

if st.button("🚀 ACTIVATE MATRIX MAPPING"):
    if user_text:
        try:
            with st.status("🔮 AI กำลังถอดรหัส Matrix...", expanded=True) as status:
                # Prompt แบบเน้นความแม่นยำสูง
                prompt = f"Analyze: '{user_text}'. Return ONLY JSON: {{'v': 0.0-1.0, 'a': 0.0-1.0, 'weather': 'Rainy/Sunny/Night', 'chords': 'string'}}"
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                
                data = json.loads(response.text)
                v = data.get('v', 0.5)
                
                # คำนวณค่า Visual จาก Matrix V2
                vis = {k: engine.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v) for k in ["SAT", "LIGHT", "CON"]}
                audio_data = engine.synthesize_audio(v, data.get('a', 0.5), data.get('weather', 'Sunny'))
                
                status.update(label="✅ การประมวลผลเสร็จสิ้น", state="complete")

            # แสดงผลลัพธ์แบบ Intelligence Dashboard
            st.markdown("<div class='matrix-box'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            col1.metric("Emotional Valence", f"{v*100:.0f}%")
            col2.metric("Energy Level", f"{data.get('a', 0)*100:.0f}%")
            col3.metric("Environment", data.get('weather'))
            
            st.write("---")
            v_col1, v_col2, v_col3 = st.columns(3)
            v_col1.write(f"**Saturation:** {vis['SAT']:.2f}")
            v_col2.write(f"**Brightness:** {vis['LIGHT']:.2f}")
            v_col3.write(f"**Contrast:** {vis['CON']:.2f}")
            
            st.audio(audio_data, format='audio/wav')
            st.caption(f"Resonance Sync: 432Hz | Matrix Chords: {data.get('chords')}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.balloons()

        except Exception as e:
            st.error(f"ระบบขัดข้อง: {e}")
    else:
        st.warning("กรุณาป้อนข้อมูลก่อนทำการ Mapping")

