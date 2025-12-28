import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import io
import time
from scipy.io import wavfile

# --- 1. CONFIGURATION ---
# ใส่ API Key ของคุณที่นี่
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. IP ASSET MATRIX (ดึงกลับมาจาก Blueprint ของคุณ) ---
MATRIX_V1 = {
    "JOY": {"F0": 0.8, "Vibrato": 0.9},
    "SAD": {"F0": 0.3, "Vibrato": 0.2}
}

MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CONTRAST": 0.8, "DOF": 0.3, "TEXTURE": 0.7, "FOCUS": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CONTRAST": 0.4, "DOF": 0.8, "TEXTURE": 0.8, "FOCUS": 0.3}
}

class UltimateAIsystem:
    def analyze_emotion(self, text):
        prompt = f"Analyze emotion/weather from: '{text}'. Return ONLY JSON: {{'v': 0.0-1.0, 'a': 0.0-1.0, 'weather': 'Rainy/Sunny/Night', 'chords': 'string'}}"
        try:
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except:
            return {"v": 0.5, "a": 0.5, "weather": "Night", "chords": "Cmaj7"}

    def lerp(self, low, high, factor): return low + (high - low) * factor

    def synthesize_audio(self, v, a, weather):
        sr = 44100
        t = np.linspace(0, 10, sr * 10)
        f0 = self.lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v)
        vibrato = self.lerp(MATRIX_V1["SAD"]["Vibrato"], MATRIX_V1["JOY"]["Vibrato"], v)
        
        # คลื่นเสียงหลัก + ฮาร์มอนิกบำบัด
        base_freq = 440 * f0
        wave = 0.5 * np.sin(2 * np.pi * base_freq * t + (vibrato * 5 * np.sin(2 * np.pi * 5 * t)))
        
        # เลเยอร์สภาพอากาศ (Weather Layer)
        noise = np.random.normal(0, 0.05, len(t))
        if weather == "Rainy":
            noise = np.convolve(noise, np.ones(50)/50, mode='same') * (1.2 - v)
        
        combined = wave + noise
        env = np.ones_like(t)
        fade = sr // 2
        env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
        return (np.clip(combined * env, -0.9, 0.9) * 32767).astype(np.int16)

# --- 3. UI DESIGN (ดึง CSS พลังงานเรืองแสงจากรูปที่ 1 กลับมา) ---
st.set_page_config(page_title="SYNAPSE Energy", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #000428, #004e92); 
        color: white;
    }
    .main-logo {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        color: #ff0055;
        text-shadow: 0 0 20px #ff0055, 0 0 40px #ff00ff;
        margin-bottom: 0px;
    }
    .sub-logo {
        text-align: center;
        font-size: 20px;
        color: #00d2ff;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #00d2ff;
        margin-top: -10px;
    }
    .slogan-box {
        text-align: center;
        background: rgba(0, 210, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(0, 210, 255, 0.3);
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        background: linear-gradient(45deg, #ff0055, #ff00ff);
        color: white;
        border: none;
        padding: 20px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(255, 0, 85, 0.7);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(255, 0, 85, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP INTERFACE (รวมโลกและพลังงาน) ---

# แสดงชื่อแอปและสโลแกนเรืองแสง
st.markdown("<div class='main-logo'>SYNAPSE</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-logo'>SOUND & VISUAL THERAPY</div>", unsafe_allow_html=True)

# ใส่รูปภาพโลโก้โลกของคุณ (ถ้าคุณอัปโหลดไฟล์รูปขึ้น GitHub)
# st.image("logo.jpg", use_column_width=True) 

st.markdown("""
    <div class='slogan-box'>
        <h3 style='color: #00d2ff; margin:0;'>\"พลังงานเพื่อโลก... อยู่นิ่งๆ ไม่เจ็บตัว\"</h3>
        <p style='margin:0; opacity: 0.8;'>STAY STILL & HEAL</p>
    </div>
    """, unsafe_allow_html=True)

# ส่วนการประมวลผล Zen Energy Charge
st.subheader("🧘 สภาวะปัจจุบัน (Zen Energy Charge)")
if st.toggle("ACTIVATE WORLD HEALING MODE"):
    bar = st.progress(0)
    for p in range(101):
        time.sleep(0.02)
        bar.progress(p)
    st.success("ชาร์จพลังงานโลกสำเร็จ! คุณได้รับพลังงานบำบัดแล้ว")

# ส่วนรับความรู้สึก
user_input = st.text_area("วันนี้สภาวะภายในและภายนอกของคุณเป็นอย่างไร?", placeholder="บอกความรู้สึกของคุณเพื่อให้ AI ปรับจูน Matrix...")

system = UltimateAIsystem()

if st.button("🚀 ACTIVATE GLOBAL ENERGY THERAPY"):
    if user_input:
        with st.status("🔮 กำลังปรับจูน Matrix V1.0 & V2.0 ตามสภาพอากาศ...", expanded=True) as status:
            data = system.analyze_emotion(user_input)
            v = data['v']
            # คำนวณค่า Visual Matrix V2.0 จริงๆ เพื่อใช้ในอนาคต
            vis = {k: system.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v) for k in MATRIX_V2["JOY"]}
            
            audio_data = system.synthesize_audio(v, data['a'], data['weather'])
            status.update(label="การบำบัดพร้อมใช้งาน", state="complete")

        # แสดง Metrics ของ Matrix
        st.write("### ⚙️ Engine Control Matrix")
        c1, c2, c3 = st.columns(3)
        c1.metric("Vocal F0 (V1.0)", f"{vis['FOCUS']:.2f}")
        c2.metric("Saturation (V2.0)", f"{vis['SAT']:.2f}")
        c3.metric("Lighting (V2.0)", f"{vis['LIGHT']:.2f}")

        # เล่นเสียงที่สร้างขึ้นมาใหม่
        st.audio(audio_data, format='audio/wav', sample_rate=44100)
        st.info(f"🔊 Resonance Mode: {data['chords']} | สภาวะแวดล้อม: {data['weather']}")
        st.balloons()
    else:
        st.warning("กรุณาพิมพ์ความรู้สึกของคุณก่อน")

st.markdown("---")
st.caption("สโลแกนของคุณ: 'อยู่นิ่งๆ ไม่เจ็บตัว' - ระบบจัดการให้เรียบร้อยครับ")
