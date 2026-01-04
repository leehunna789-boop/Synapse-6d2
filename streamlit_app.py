import streamlit as st
import google.generativeai as genai
import numpy as np
import soundfile as sf
import json
import re
from scipy import signal
import time
from PIL import Image  # <--- ตัวสำคัญสำหรับโหลดรูป

# --- [1. โหลด LOGO & ตั้งค่าหน้าจอ] ---
try:
    # พยายามโหลดไฟล์รูป logo.jpg
    logo_img = Image.open("logo.jpg")
except:
    # ถ้าหาไม่เจอ ให้ใช้อิโมจิแทน (กันโปรแกรมพัง)
    logo_img = "💠"

st.set_page_config(
    page_title="SYNAPSE: NEO",
    page_icon=logo_img,  # <--- ใส่รูปตรงหัว Tab Browser
    layout="wide"
)

# --- [2. DESIGN SYSTEM (Dark Theme)] ---
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .stTextInput > div > div > input { background-color: #0a0a0a; color: #00ff41; border: 1px solid #333; }
    .stButton > button { background-color: #000; color: #00ff41; border: 1px solid #00ff41; text-transform: uppercase; font-weight: bold; }
    .stButton > button:hover { background-color: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    h1 { text-shadow: 0 0 10px #00ff41; border-bottom: 2px solid #333; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- [3. SYSTEM CHECK] ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⛔ SYSTEM HALTED: INSERT API KEY")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ค้นหาโมเดลอัตโนมัติ (กัน Error 404)
@st.cache_resource
def get_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'gemini' in m.name: return m.name
    return "models/gemini-pro"

model_name = get_model()
model = genai.GenerativeModel(model_name)

# --- [4. AUDIO ENGINE] ---
def neo_engine(duration, fs, params):
    t = np.linspace(0, duration, int(fs * duration))
    freq = params.get('frequency', 174)
    beat = params.get('binaural_beat', 6)
    wave_type = params.get('waveform', 'sine')
    
    def generate_wave(f, type):
        if type == 'saw': return signal.sawtooth(2 * np.pi * f * t)
        elif type == 'square': return signal.square(2 * np.pi * f * t)
        else: return np.sin(2 * np.pi * f * t)

    left = 0.5 * generate_wave(freq, wave_type)
    right = 0.5 * generate_wave(freq + beat, wave_type)
    noise = np.random.normal(0, 0.005, len(t))
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t)
    return np.vstack((left*lfo + noise, right*lfo + noise)).T * 0.4

# --- [5. UI: THE COCKPIT] ---
# แบ่งคอลัมน์: รูป Logo อยู่ซ้าย, ชื่อแอปอยู่ขวา
col1, col2 = st.columns([1, 5])

with col1:
    # แสดงรูปโลโก้บนหน้าจอ
    try:
        st.image("logo.jpg", width=120) 
    except:
        st.write("💠") # ถ้าหารูปไม่เจอ

with col2:
    st.markdown("# 💠 SYNAPSE // NEO")
    st.caption(f"SYSTEM ONLINE | MODEL: {model_name}")

st.markdown("---")

user_input = st.text_input(">> INPUT NEURAL DATA (พิมพ์ความรู้สึก):")

if st.button("INITIATE PROTOCOL"):
    if not user_input:
        st.warning("⚠️ DATA MISSING")
    else:
        # Progress Bar เท่ๆ
        progress_text = "Establishing Neural Link..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=f"PROCESSING: {percent_complete}%")
        my_bar.empty()

        try:
            prompt = f"""
            Analyze emotion: "{user_input}"
            Return ONLY JSON with:
            1. "frequency": (float 100-800)
            2. "binaural_beat": (float 1-15)
            3. "waveform": ("sine", "saw", "square")
            4. "message": (Thai quote ending with "อยู่นิ่งๆ ไม่เจ็บตัว")
            """
            
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if match:
                ai_data = json.loads(match.group())
                
                # Dashboard
                c1, c2, c3 = st.columns(3)
                c1.metric("FREQ", f"{ai_data['frequency']} Hz")
                c2.metric("BEAT", f"{ai_data['binaural_beat']} Hz")
                c3.metric("WAVE", ai_data['waveform'].upper())
                
                # Audio
                y = neo_engine(60, 44100, ai_data)
                sf.write("neo.wav", y, 44100)
                
                st.markdown("### 🔊 AUDIO OUTPUT")
                st.audio("neo.wav")
                st.success(f"📟 {ai_data['message']}")
            else:
                st.error("❌ DATA PARSING ERROR")
                
        except Exception as e:
            st.error(f"⛔ ERROR: {e}")
            st.info("💡 หมายเหตุ: ถ้าขึ้น Error 429 แปลว่าโควต้าวันนี้หมดนะครับ ต้องรอพรุ่งนี้หรือเปลี่ยน Key ใหม่")
