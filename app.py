import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import io
from scipy.io import wavfile

# --- 1. CONFIGURATION (กรุณาใส่ API Key ของคุณ) ---
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. IP ASSET MATRIX (V1.0 & V2.0) ---
# ข้อมูลจาก Blueprint มูลค่าสูงที่คุณออกแบบไว้
MATRIX_V1 = {
    "JOY": {"F0": 0.8, "Vibrato": 0.9},
    "SAD": {"F0": 0.3, "Vibrato": 0.2}
}

MATRIX_V2 = {
    "JOY": {
        "SAT": 0.9, "LIGHT": 0.8, "CONTRAST": 0.8, 
        "DOF": 0.3, "TEXTURE": 0.7, "FOCUS": 0.9
    },
    "SAD": {
        "SAT": 0.2, "LIGHT": 0.3, "CONTRAST": 0.4, 
        "DOF": 0.8, "TEXTURE": 0.8, "FOCUS": 0.3
    }
}

class UltimateAIsystem:
    """ระบบหลักที่รวบรวม AI 5 ตัวเข้าด้วยกัน (Analysis -> Synthesis -> Mastering)"""
    
    def analyze_emotion_gemini(self, user_text):
        """AI ตัวที่ 1: วิเคราะห์อารมณ์และสภาพอากาศ (Output เป็น JSON เสมอ)"""
        prompt = f"""
        วิเคราะห์อารมณ์จากข้อความ: '{user_text}' 
        ตอบเป็น JSON เท่านั้น ห้ามบรรยาย:
        {{
            "v": 0.0-1.0 (ความสุข), 
            "a": 0.0-1.0 (พลังงาน), 
            "weather": "Rainy" | "Sunny" | "Night" | "Windy",
            "chords": "string"
        }}
        """
        try:
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except:
            # Fallback หาก API มีปัญหา
            return {"v": 0.5, "a": 0.5, "weather": "Night", "chords": "Cmaj7"}

    def lerp(self, low, high, factor):
        """Linear Interpolation เพื่อความสมูทของ Matrix"""
        return low + (high - low) * factor

    def synthesize_music_pro(self, v, a, weather):
        """AI ตัวที่ 2-4: สร้างเสียงแบบ Parametric ตาม Matrix V1.0 และสภาพอากาศ"""
        sr = 44100
        duration = 10 # เล่นยาว 10 วินาที
        t = np.linspace(0, duration, sr * duration)
        
        # ค้นหาค่าจาก Matrix V1.0 ด้วย Lerp
        f0_scalar = self.lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v)
        vibrato_rate = self.lerp(MATRIX_V1["SAD"]["Vibrato"], MATRIX_V1["JOY"]["Vibrato"], v)
        
        # 1. Base Melody (Sine Wave + Harmonics)
        base_freq = 440 * f0_scalar
        vibrato = (vibrato_rate * 5) * np.sin(2 * np.pi * 5 * t)
        wave = 0.5 * np.sin(2 * np.pi * base_freq * t + vibrato)
        overtone = 0.2 * np.sin(2 * np.pi * (base_freq * 2) * t)
        
        # 2. Weather Layer (Simulated Nature Sound)
        noise = np.random.normal(0, 0.1, len(t))
        if weather == "Rainy":
            weather_layer = np.convolve(noise, np.ones(50)/50, mode='same') * (1.2 - v)
        elif weather == "Windy":
            weather_layer = noise * (0.5 * (1 + np.sin(2 * np.pi * 0.2 * t)))
        else:
            weather_layer = noise * 0.02

        # 3. Binaural Beats (Alpha Wave สำหรับการบำบัด)
        binaural = 0.05 * np.sin(2 * np.pi * (base_freq + 10) * t)
        
        combined = wave + overtone + weather_layer + binaural
        
        # Fade In/Out ป้องกันเสียงบาดหู
        env = np.ones_like(t)
        fade_len = sr // 2
        env[:fade_len] = np.linspace(0, 1, fade_len)
        env[-fade_len:] = np.linspace(1, 0, fade_len)
        
        return (np.clip(combined * env, -0.9, 0.9) * 32767).astype(np.int16)

# --- 3. STREAMLIT UI DESIGN ---
st.set_page_config(page_title="SYNAPSE AI Therapy", layout="wide")
system = UltimateAIsystem()

# ตกแต่ง CSS ให้ดูเป็น Energy Therapy
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #58a6ff; border: 1px solid #30363d; }
    .glow-text { color: #00d2ff; text-shadow: 0 0 10px #00d2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 SYNAPSE: Energy for the World")
st.markdown("<div class='glow-text'>พลังงานเพื่อโลก... อยู่นิ่งๆ ไม่เจ็บตัว</div>", unsafe_allow_html=True)

# ส่วนรับ Input
user_input = st.text_area("วันนี้สภาวะของคุณเป็นอย่างไร?", placeholder="เช่น วันนี้เหนื่อยจัง แต่อากาศข้างนอกสดใสมาก...")

if st.button("🚀 ACTIVATE GLOBAL ENERGY THERAPY"):
    if user_input:
        with st.status("🔮 กำลังประมวลผล Matrix ตามสภาพอากาศและอารมณ์...", expanded=True) as status:
            # 1. วิเคราะห์ด้วย Gemini
            data = system.analyze_emotion_gemini(user_input)
            st.write(f"✅ ตรวจพบอารมณ์ (Valence): {data['v']:.2f}")
            st.write(f"🌤️ สภาพอากาศในใจ: {data['weather']}")
            
            # 2. คำนวณ Visual Matrix V2.0
            v_val = data['v']
            visual = {k: system.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v_val) for k in MATRIX_V2["JOY"]}
            
            # 3. สังเคราะห์เสียง
            audio_data = system.synthesize_music_pro(v_val, data['a'], data['weather'])
            
            status.update(label="✅ การบำบัดพร้อมใช้งานแล้ว", state="complete")

        # แสดงผล Visual Metrics (V2.0)
        st.subheader("🎨 Visual Parameter Sync (Matrix V2.0)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Saturation", f"{visual['SAT']:.2f}")
        col2.metric("Key Light", f"{visual['LIGHT']:.2f}")
        col3.metric("Contrast", f"{visual['CONTRAST']:.2f}")
        col4.metric("Focus", f"{visual['FOCUS']:.2f}")

        # แสดงผล Audio
        st.subheader(f"🔊 Healing Soundscape: {data['chords']}")
        st.audio(audio_data, format='audio/wav', sample_rate=44100)
        
        # ระบบดาวน์โหลดไฟล์
        virtual_file = io.BytesIO()
        wavfile.write(virtual_file, 44100, audio_data)
        st.download_button("⬇️ เก็บพลังงานนี้ไว้ (Download WAV)", virtual_file.getvalue(), "synapse_therapy.wav", "audio/wav")
        
        st.info("คำแนะนำ: หลับตาลง ปล่อยกายใจให้ว่าง และ 'อยู่นิ่งๆ' เพื่อรับพลังงานบำบัด")
    else:
        st.warning("กรุณาพิมพ์ความรู้สึกของคุณก่อนเริ่มการบำบัด")

st.sidebar.title("🛠️ System Engine")
st.sidebar.write("Version: IP Asset 3D Matrix V2.1")
st.sidebar.markdown("---")
st.sidebar.info("ระบบจะใช้ Linear Interpolation เพื่อให้เสียงและภาพเปลี่ยนตามอารมณ์ของคุณอย่างนุ่มนวลที่สุด")
