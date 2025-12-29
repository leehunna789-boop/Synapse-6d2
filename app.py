import numpy as np
import streamlit as st
from scipy.io import wavfile
import io
import google.generativeai as genai

# --- การตั้งค่า API และโมเดล ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("กรุณาตรวจสอบการตั้งค่า GEMINI_API_KEY ใน Secrets")

# -----------------------------------------------------------
# 1. INPUT MODULE (เชื่อมต่อ AI เพื่อวิเคราะห์ดนตรี)
# -----------------------------------------------------------
class InputModule:
    ROOT_VOCAB = {"C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63, "F": 349.23, 
                  "F#": 369.99, "G": 392.00, "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88} 

    def ให้_AI_วิเคราะห์_Rhythm(self, chords, valence, arousal):
        """ใช้ Gemini API ช่วยกำหนดความเร็วและสไตล์เพลง"""
        prompt = f"วิเคราะห์คอร์ด {chords} อารมณ์ (Valence={valence}, Arousal={arousal}) แนะนำความเร็วเพลง (BPM) และสไตล์สั้นๆ"
        try:
            response = model.generate_content(prompt)
            return response.text
        except:
            return "ไม่สามารถเชื่อมต่อ AI ได้ (ใช้ค่ามาตรฐาน)"

    def จัด_โครงสร้าง_คำสั่ง(self, คำสั่งคอร์ด, valence, arousal):
        chords = [c.strip().split()[0].upper() for c in คำสั่งคอร์ด.split(',') if c.strip()]
        chord_freqs = [self.ROOT_VOCAB.get(c, 261.63) for c in chords]
        
        # Symbolic Sequence: [Frequency, Valence, Arousal]
        return np.array([[f, valence, arousal] for f in chord_freqs])

# -----------------------------------------------------------
# 2. AI SYNTHESIS ENGINE (สร้างเสียงตามคุณลักษณะ RBF)
# -----------------------------------------------------------
class AISynthesisEngine:
    def __init__(self, samplerate=44100):
        self.sampling_rate = samplerate

    def สังเคราะห์_เสียง(self, symbolic_sequence):
        final_audio = np.array([], dtype=np.float32)
        
        for row in symbolic_sequence:
            freq, valence, arousal = row
            # ปรับความยาวโน้ตตาม Arousal (ยิ่งสูงยิ่งสั้น/กระชับ)
            duration = 0.8 - (arousal * 0.4) 
            t = np.linspace(0, duration, int(self.sampling_rate * duration), endpoint=False)
            
            # สร้างเสียง Synth พื้นฐาน
            amplitude = 0.2 + (arousal * 0.5)
            # ผสมคลื่น Sine และ Square เล็กน้อยเพื่อให้มี Harmonic (ถ้า Valence สูงจะนุ่มนวล)
            wave = (1-valence)*0.5 * np.sin(2 * np.pi * freq * t) + (valence)*0.5 * np.cos(2 * np.pi * freq * t)
            
            # ใส่ ADSR Envelope เบื้องต้น (Fade in/out)
            fade = int(self.sampling_rate * 0.05)
            envelope = np.ones_like(wave)
            envelope[:fade] = np.linspace(0, 1, fade)
            envelope[-fade:] = np.linspace(1, 0, fade)
            
            final_audio = np.concatenate([final_audio, wave * amplitude * envelope])
            
        return final_audio

# -----------------------------------------------------------
# 3. STREAMLIT UI
# -----------------------------------------------------------
st.set_page_config(layout="wide", page_title="RBF AI Synthesizer")
st.title("🎼 RBF AI Music Engine (API Connected)")

# Sidebar สำหรับ Logs
st.sidebar.header("⚙️ System Status")

# --- UI Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎹 Input Parameters")
    chords = st.text_input("คอร์ด (เช่น C, Am, F, G)", "C, Am, F, G")
    v = st.slider("ความสุข (Valence)", 0.0, 1.0, 0.7)
    a = st.slider("พลังงาน (Arousal)", 0.0, 1.0, 0.5)
    
    btn = st.button("🚀 สังเคราะห์เพลง", type="primary")

with col2:
    if btn:
        system = InputModule()
        engine = AISynthesisEngine()
        
        with st.spinner("AI กำลังวิเคราะห์ดนตรี..."):
            # เรียกใช้ API
            ai_advice = system.ให้_AI_วิเคราะห์_Rhythm(chords, v, a)
            st.info(f"🤖 **AI Advice:** {ai_advice}")
            
            # ประมวลผลเสียง
            sym_seq = system.จัด_โครงสร้าง_คำสั่ง(chords, v, a)
            raw_audio = engine.สังเคราะห์_เสียง(sym_seq)
            
            st.subheader("🎵 Result")
            st.line_chart(raw_audio[:5000]) # แสดง Waveform
            st.audio(raw_audio, sample_rate=44100)
            
            # ปุ่มดาวน์โหลด
            buffer = io.BytesIO()
            wavfile.write(buffer, 44100, (raw_audio * 32767).astype(np.int16))
            st.download_button("⬇️ Download WAV", buffer, "rbf_music.wav")
            
            st.sidebar.success("การสังเคราะห์เสร็จสมบูรณ์!")
    else:
        st.write("รอรับคำสั่งจากคุณอยู่ครับ...")

st.sidebar.markdown("---")
st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")
