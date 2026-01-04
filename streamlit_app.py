import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import io
from scipy.io import wavfile
from PIL import Image 

# --- 1. CONFIGURATION & LOGO ---
st.set_page_config(page_title="SYNAPSE: Therapy", layout="wide", page_icon="💠")

# ส่วนโหลดโลโก้ (ใส่ให้แล้วครับ)
try:
    logo_img = Image.open("logo.jpg")
    st.image(logo_img, width=120)
except:
    pass # ถ้าไม่มีรูปก็ข้ามไป ไม่พัง

# ส่วนแก้ API Key (แก้ให้แล้วครับ)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⛔ กรุณาใส่ API Key ใน Settings -> Secrets ก่อนครับ")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. IP ASSET MATRIX (V1.0 & V2.0) ---
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
    """ระบบหลักที่รวบรวม AI 5 ตัวเข้าด้วยกัน"""
    
    def analyze_emotion_gemini(self, user_text):
        """AI ตัวที่ 1: วิเคราะห์อารมณ์"""
        prompt = f"""
        วิเคราะห์อารมณ์จากข้อความ: '{user_text}' 
        ตอบเป็น JSON เท่านั้น ห้ามบรรยาย:
        {{
            "v": (float 0.0-1.0 ความสุข), 
            "a": (float 0.0-1.0 พลังงาน), 
            "weather": "Rainy" | "Sunny" | "Night" | "Windy",
            "chords": "string"
        }}
        """
        try:
            response = model.generate_content(prompt)
            # แก้ไขการดึง JSON ให้แม่นยำขึ้น
            import re
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group())
            else:
                return {"v": 0.5, "a": 0.5, "weather": "Night", "chords": "Cmaj7"}
        except:
            return {"v": 0.5, "a": 0.5, "weather": "Night", "chords": "Cmaj7"}

    def lerp(self, low, high, factor):
        return low + (high - low) * factor

    def synthesize_music_pro(self, v, a, weather):
        """AI ตัวที่ 2-4: สร้างเสียง"""
        sr = 44100
        duration = 10 
        t = np.linspace(0, duration, sr * duration)
        
        f0_scalar = self.lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v)
        vibrato_rate = self.lerp(MATRIX_V1["SAD"]["Vibrato"], MATRIX_V1["JOY"]["Vibrato"], v)
        
        base_freq = 440 * f0_scalar
        vibrato = (vibrato_rate * 5) * np.sin(2 * np.pi * 5 * t)
        wave = 0.5 * np.sin(2 * np.pi * base_freq * t + vibrato)
        overtone = 0.2 * np.sin(2 * np.pi * (base_freq * 2) * t)
        
        noise = np.random.normal(0, 0.1, len(t))
        if weather == "Rainy":
            weather_layer = np.convolve(noise, np.ones(50)/50, mode='same') * (1.2 - v)
        elif weather == "Windy":
            weather_layer = noise * (0.5 * (1 + np.sin(2 * np.pi * 0.2 * t)))
        else:
            weather_layer = noise * 0.02

        binaural = 0.05 * np.sin(2 * np.pi * (base_freq + 10) * t)
        
        combined = wave + overtone + weather_layer + binaural
        
        env = np.ones_like(t)
        fade_len = sr // 2
        env[:fade_len] = np.linspace(0, 1, fade_len)
        env[-fade_len:] = np.linspace(1, 0, fade_len)
        
        return (np.clip(combined * env, -0.9, 0.9) * 32767).astype(np.int16)

# --- 3. UI SETUP ---
system = UltimateAIsystem()

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #161b22; color: #58a6ff; border: 1px solid #30363d; }
    .glow-text { color: #00d2ff; text-shadow: 0 0 10px #00d2ff; font-weight: bold; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 SYNAPSE: Energy Therapy")
st.markdown("<div class='glow-text'>พลังงานเพื่อโลก... อยู่นิ่งๆ ไม่เจ็บตัว</div>", unsafe_allow_html=True)

user_input = st.text_area("วันนี้สภาวะของคุณเป็นอย่างไร?", placeholder="เช่น วันนี้เหนื่อยจัง แต่อากาศข้างนอกสดใสมาก...")

if st.button("🚀 ACTIVATE GLOBAL ENERGY THERAPY"):
    if user_input:
        with st.status("🔮 กำลังประมวลผล Matrix...", expanded=True) as status:
            data = system.analyze_emotion_gemini(user_input)
            st.write(f"✅ ตรวจพบอารมณ์: {data.get('v', 0.5):.2f}")
            st.write(f"🌤️ สภาพอากาศในใจ: {data.get('weather', 'Normal')}")
            
            v_val = data.get('v', 0.5)
            # แก้ไข bug การดึงค่า dict
            visual = {k: system.lerp(MATRIX_V2["SAD"][k], MATRIX_V2["JOY"][k], v_val) for k in MATRIX_V2["JOY"]}
            
            audio_data = system.synthesize_music_pro(v_val, data.get('a', 0.5), data.get('weather', 'Normal'))
            
            status.update(label="✅ การบำบัดพร้อมใช้งานแล้ว", state="complete")

        st.subheader("🎨 Visual Parameter Sync (Matrix V2.0)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Saturation", f"{visual['SAT']:.2f}")
        c2.metric("Key Light", f"{visual['LIGHT']:.2f}")
        c3.metric("Contrast", f"{visual['CONTRAST']:.2f}")
        c4.metric("Focus", f"{visual['FOCUS']:.2f}")

        st.subheader(f"🔊 Healing Soundscape: {data.get('chords', 'C')}")
        st.audio(audio_data, format='audio/wav', sample_rate=44100)
        
        # ปุ่มโหลด
        virtual_file = io.BytesIO()
        wavfile.write(virtual_file, 44100, audio_data)
        st.download_button("⬇️ เก็บพลังงานนี้ไว้", virtual_file.getvalue(), "synapse_therapy.wav", "audio/wav")
        
        st.success("ข้อคิด: อยู่นิ่งๆ ไม่เจ็บตัว")
    else:
        st.warning("กรุณาพิมพ์ความรู้สึกก่อนเริ่มครับ")
