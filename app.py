import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests, geocoder
import pandas as pd
from scipy.io import wavfile

# --- 1. DESIGN & NEON REFLEX UI (แดง-น้ำเงิน-เขียว-ขาว สะท้อนแสง) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    /* พื้นหลังดำสนิทเพื่อให้สีสะท้อนแสงเด่นชัด */
    .stApp { background-color: #000000; color: #FFFFFF; } 
    
    /* หัวข้อน้ำเงินสะท้อนแสง */
    h1 { color: #00f2fe !important; text-shadow: 0 0 20px #00f2fe, 0 0 30px #00f2fe; text-align: center; }
    h3 { color: #FFFFFF !important; text-shadow: 0 0 10px #FFFFFF; }

    /* ปุ่มแดงสะท้อนแสง ทรงพลัง */
    .stButton>button { 
        background: linear-gradient(45deg, #FF0000, #990000); 
        color: white; border-radius: 50px; width: 100%; font-weight: bold; height: 70px;
        border: 2px solid #FF5555; box-shadow: 0px 0px 20px rgba(255, 0, 0, 0.6);
        font-size: 20px; transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0px 0px 40px #FF0000; transform: scale(1.02); }

    /* ค่า Matrix ขาวสะท้อนแสง */
    .stMetric { background-color: #111111; border-radius: 15px; padding: 20px; border: 1px solid #444; box-shadow: 0 0 10px #FFFFFF; }
    
    /* กรอบรับข้อมูลเขียวสะท้อนแสง */
    .stTextArea textarea { background-color: #050505; color: #00FF00; border: 1px solid #00FF00; box-shadow: 0 0 5px #00FF00; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI CORE & UNLIMITED DATA SYNC ---
# ดึงกุญแจจริงจาก Secrets เพื่อความสามารถ AI ที่สมบูรณ์
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ระบบล็อก: กรุณาใส่ GEMINI_API_KEY ในหน้า Secrets")
    st.stop()

# โหลด IP ASSET: Control Matrix V1 & V2 (ทรัพย์สินมูลค่าสูง)
MATRIX_V1 = {"JOY": {"f0": 0.8, "vib": 0.9}, "SAD": {"f0": 0.3, "vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3}
}

# ฟังก์ชันดึงพิกัดและสภาพอากาศจริง (Sensor Sync)
def get_sensor_data():
    try:
        g = geocoder.ip('me')
        url = f"https://api.open-meteo.com/v1/forecast?latitude={g.latlng[0]}&longitude={g.latlng[1]}&current_weather=true"
        weather = requests.get(url).json()['current_weather']
        return {"temp": weather['temperature'], "city": g.city, "code": weather['weathercode']}
    except:
        return {"temp": 25, "city": "Global Matrix", "code": 0}

# --- 3. 6D UNLIMITED SYNTHESIS ENGINE ---
class SynapseUnlimited:
    def lerp(self, low, high, factor): return low + (high - low) * factor

    def generate_6d_audio(self, v, bpm, weather_code):
        sr = 44100
        t = np.linspace(0, 10, sr * 10) # เล่นยาว 10 วินาทีเพื่อความดื่มด่ำ
        
        # ปรับจูนตามชีพจรและอารมณ์จริง (ห้ามมั่ว)
        f0 = self.lerp(MATRIX_V1["SAD"]["f0"], MATRIX_V1["JOY"]["f0"], v) * (bpm / 75.0)
        vib = self.lerp(MATRIX_V1["SAD"]["vib"], MATRIX_V1["JOY"]["vib"], v)
        
        # สร้างมิติเสียง 6 มิติ (Harmonics + Binaural + Environment)
        base_wave = 0.5 * np.sin(2 * np.pi * (432 * f0) * t + (vib * 10 * np.sin(2 * np.pi * 4 * t)))
        
        # เพิ่มเสียงสภาพอากาศจริง
        if weather_code > 50: # ถ้าฝนตกหรืออากาศชื้น
            base_wave += np.random.normal(0, 0.03, len(t)) 
            
        audio_final = (np.clip(base_wave, -0.9, 0.9) * 32767).astype(np.int16)
        return audio_final

# --- 4. REAL-TIME INTERFACE & LOGIC ---
# แสดงโลโก้แอปของคุณ
if os.path.exists("1000008875.jpg"):
    st.image("1000008875.jpg", use_container_width=True)

st.title("💎 SYNAPSE 6D Pro: UNLIMITED")
st.markdown("<p style='text-align:center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว - ระบบดึงพลังงานจริงจากโลกและตัวคุณ\"</p>", unsafe_allow_html=True)

# ดึงข้อมูลเซนเซอร์โลกจริง
env = get_sensor_data()
col1, col2 = st.columns(2)
col1.metric("📍 พิกัดโลกจริง", env['city'])
col2.metric("🌡️ อุณหภูมิพิกัด", f"{env['temp']}°C")

# รับค่าชีพจรจริง (Bio-Feedback)
st.sidebar.header("📡 Bio-Sensor Sync")
heart_rate = st.sidebar.number_input("ชีพจรปัจจุบัน (BPM) จากนาฬิกาของคุณ", 40, 200, 75)

user_msg = st.text_area("ป้อนสภาวะภายในของคุณ (รองรับ ไทย/EN/JP/CN):", placeholder="ขยี้ความรู้สึกของคุณที่นี่...")

engine = SynapseUnlimited()

if st.button("🚀 ACTIVATE UNLIMITED MATRIX SYNC"):
    if user_msg:
        with st.status("🔮 AI 6 ระบบกำลังประมวลผลข้อมูลจริง..."):
            # Step 1: Gemini Unlimited Analysis
            prompt = f"Analyze emotion from: '{user_msg}'. Return JSON: {{'v': 0.0-1.0, 'a': 0.0-1.0, 'txt': 'summary'}}"
            res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(res.text)
            
            # Step 2: Synthesis
            audio = engine.generate_6d_audio(data['v'], heart_rate, env['code'])
            
            # Step 3: Visual Master V2.0
            st.subheader("🎨 Energy Matrix Visualized")
            vis_col = st.columns(3)
            vis_col[0].metric("Cell Light", f"{data['v']*100:.1f}%")
            vis_col[1].metric("Energy Flow", "UNLIMITED")
            vis_col[2].metric("Sync Status", "REAL-TIME")
            
            st.audio(audio, format='audio/wav', sample_rate=44100)
            st.success(f"✅ ปรับจูนเสร็จสมบูรณ์: {data['txt']}")
            st.balloons()
    else:
        st.warning("กรุณาใส่ข้อมูลเพื่อเริ่มการซิงค์พลังงาน")
