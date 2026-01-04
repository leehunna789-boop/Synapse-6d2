import streamlit as st
import google.generativeai as genai
import numpy as np
import soundfile as sf
import json
import re
from scipy import signal # เพิ่มไลบรารีสร้างคลื่นเสียงแปลกๆ

st.set_page_config(page_title="SYNAPSE: DYNAMIC", page_icon="🎛️")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("⛔ ไม่พบ API Key")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- [ค้นหาโมเดลอัตโนมัติ] ---
@st.cache_resource
def get_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'gemini' in m.name: return m.name
    return "models/gemini-pro"

model_name = get_model()
model = genai.GenerativeModel(model_name)

# --- [ENGINE ใหม่: เปลี่ยนเนื้อเสียงได้ (Timbre Control)] ---
def dynamic_engine(duration, fs, params):
    t = np.linspace(0, duration, int(fs * duration))
    freq = params.get('frequency', 174)
    beat = params.get('binaural_beat', 6)
    wave_type = params.get('waveform', 'sine') # <--- รับค่าชนิดเสียงจาก AI
    
    # ฟังก์ชันสร้างคลื่นตามคำสั่ง AI
    def generate_wave(f, type):
        if type == 'saw': 
            return signal.sawtooth(2 * np.pi * f * t) # เสียงแตก (Industrial)
        elif type == 'square':
            return signal.square(2 * np.pi * f * t)   # เสียงหุ่นยนต์ (Retro)
        else:
            return np.sin(2 * np.pi * f * t)          # เสียงนุ่ม (Pure)

    # สร้างเสียงซ้ายขวา
    left = 0.5 * generate_wave(freq, wave_type)
    right = 0.5 * generate_wave(freq + beat, wave_type)
    
    # Effect หายใจ (LFO)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t)
    
    return np.vstack((left*lfo, right*lfo)).T * 0.3 # ลดเสียงลงนิดนึงกันลำโพงแตก

# --- [UI] ---
st.title(f"🎛️ SYNAPSE: Texture Change")
st.caption(f"Connected to: {model_name}")

user_input = st.text_input("พิมพ์อารมณ์ของคุณ (เช่น: เกลียด, รัก, ว่างเปล่า):")

if st.button("EXECUTE"):
    if user_input:
        with st.status("🧠 AI กำลังเลือกเครื่องดนตรี...", expanded=True):
            try:
                # Prompt ใหม่: สั่งให้เลือก waveform ด้วย
                prompt = f"""
                Analyze emotion: "{user_input}"
                Return ONLY JSON with:
                1. "frequency": (float 100-800)
                2. "binaural_beat": (float 1-15)
                3. "waveform": (string, choose one: "sine", "saw", "square")
                   - Use "sine" for peace, sad, calm.
                   - Use "saw" for anger, pain, energy, industrial.
                   - Use "square" for confusion, robot, digital.
                4. "message": (Thai quote)
                """
                
                response = model.generate_content(prompt)
                
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if match:
                    ai_data = json.loads(match.group())
                    
                    # โชว์ให้เห็นเลยว่า AI เลือกเสียงแบบไหน
                    st.write("---")
                    c1, c2 = st.columns(2)
                    c1.metric("Frequency", f"{ai_data['frequency']} Hz")
                    c2.metric("Waveform Type", ai_data['waveform'].upper()) # <--- ดูตรงนี้
                    
                    if ai_data['waveform'] == 'sine':
                        st.info("🌊 Selected: เสียงนุ่ม (Sine)")
                    elif ai_data['waveform'] == 'saw':
                        st.warning("⚡ Selected: เสียงแตก (Sawtooth)")
                    else:
                        st.success("🤖 Selected: เสียงดิจิตอล (Square)")

                    # สร้างเสียง
                    y = dynamic_engine(60, 44100, ai_data)
                    sf.write("dynamic.wav", y, 44100)
                    
                    st.audio("dynamic.wav")
                    st.write(f"💬 {ai_data['message']}")
                else:
                    st.error("AI ส่งข้อมูลผิดพลาด")
            except Exception as e:
                st.error(f"Error: {e}")
