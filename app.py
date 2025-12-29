import numpy as np
import streamlit as st
from scipy.io import wavfile
import io

# ===========================================================
# RBF AI MUSIC SYNTHESIZER (SINGLE-FILE VERSION)
# ===========================================================

# --- 1. CONFIG & SECRETS ---
st.set_page_config(layout="wide", page_title="RBF AI Synthesizer")

# ดึง API Key มาเก็บไว้ในตัวแปร (สำหรับเตรียมใช้ในอนาคตตามที่คุณมีใน Secrets)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    key_status = "✅ API Key Loaded & Standby"
except Exception:
    API_KEY = None
    key_status = "⚠️ No API Key in Secrets (Local Mode Only)"

# --- 2. CORE ENGINE MODULES ---

class RBAISystem:
    def __init__(self):
        # ความถี่โน้ตมาตรฐาน
        self.FREQ_MAP = {
            "C": 261.63, "C#": 277.18, "Db": 277.18, "D": 293.66, "D#": 311.13, 
            "Eb": 311.13, "E": 329.63, "F": 349.23, "F#": 369.99, "Gb": 369.99, 
            "G": 392.00, "G#": 415.30, "Ab": 415.30, "A": 440.00, "A#": 466.16, 
            "Bb": 466.16, "B": 493.88
        }
        self.fs = 44100  # Sampling Rate

    def generate_audio(self, chord_input, valence, arousal):
        # --- [STAGE 1: INPUT PROCESSING] ---
        chords = [c.strip().capitalize() for c in chord_input.split(',') if c.strip()]
        if not chords: chords = ["C"]
        
        final_audio = np.array([], dtype=np.float32)

        # --- [STAGE 2: AI SYNTHESIS (RBF LOGIC)] ---
        for chord_name in chords:
            # ดึง Root Note Frequency
            root = chord_name[:2].strip() if len(chord_name)>1 and chord_name[1]=='#' else chord_name[0]
            freq = self.FREQ_MAP.get(root, 261.63)
            
            # RBF: Arousal กำหนดความยาว (High Arousal = Short/Fast notes)
            duration = 1.2 - (arousal * 0.8) 
            t = np.linspace(0, duration, int(self.fs * duration), endpoint=False)
            
            # RBF: Valence กำหนดเนื้อเสียง (Timbre)
            # High Valence = Sine (Smooth), Low Valence = Sawtooth (Rough/Gritty)
            smooth_wave = np.sin(2 * np.pi * freq * t)
            rough_wave = 2 * (t * freq - np.floor(0.5 + t * freq))
            
            # ผสมคลื่นเสียงตามค่า Valence
            combined_wave = (valence * smooth_wave) + ((1 - valence) * rough_wave)
            
            # RBF: Arousal กำหนดความดัง (Amplitude)
            amp = 0.1 + (arousal * 0.5)
            
            # --- [STAGE 3: MASTERING (ENVELOPE & LIMITER)] ---
            # ป้องกันเสียงคลิกด้วย ADSR ง่ายๆ (Fade In/Out)
            fade = int(self.fs * 0.05)
            envelope = np.ones_like(combined_wave)
            envelope[:fade] = np.linspace(0, 1, fade)
            envelope[-fade:] = np.linspace(1, 0, fade)
            
            processed_note = combined_wave * amp * envelope
            final_audio = np.concatenate([final_audio, processed_note])

        # ป้องกัน Clipping (Limiter)
        final_audio = np.clip(final_audio, -0.9, 0.9)
        return final_audio

# --- 3. STREAMLIT UI ---

st.title("🎼 RBF AI Music Synthesizer")
st.sidebar.title("🛠️ System Info")
st.sidebar.info(f"API Status: {key_status}")
st.sidebar.markdown("---")
st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")

# Layout สำหรับ Input
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        chord_text = st.text_input("ป้อนลำดับคอร์ด (คั่นด้วยเครื่องหมาย , )", "C, Am, F, G")
    with col2:
        val_val = st.slider("Valence (ความนุ่มนวล)", 0.0, 1.0, 0.7)
    with col3:
        aro_val = st.slider("Arousal (พลังงาน)", 0.0, 1.0, 0.5)

# ปุ่มกดสังเคราะห์
if st.button("🚀 สังเคราะห์และมาสเตอร์เสียงทันที", type="primary"):
    system = RBAISystem()
    
    with st.spinner("กำลังคำนวณคลื่นเสียงแบบ RBF..."):
        audio_data = system.generate_audio(chord_text, val_val, aro_val)
        
        st.success("สร้างเสียงเสร็จสมบูรณ์!")
        
        # แสดงผล Waveform
        st.subheader("📊 Audio Waveform")
        st.line_chart(audio_data[:5000]) 
        
        # ส่วนควบคุมการเล่นเสียง
        st.subheader("🔊 Playback")
        st.audio(audio_data, sample_rate=44100)
        
        # ส่วนดาวน์โหลด
        buffer = io.BytesIO()
        # แปลงเป็น 16-bit PCM สำหรับไฟล์ WAV
        audio_int16 = (audio_data * 32767).astype(np.int16)
        wavfile.write(buffer, 44100, audio_int16)
        
        st.download_button(
            label="⬇️ ดาวน์โหลดไฟล์ WAV",
            data=buffer.getvalue(),
            file_name="rbf_ai_music.wav",
            mime="audio/wav"
        )
else:
    st.info("กรุณาป้อนคอร์ดแล้วกดปุ่มด้านบน เพื่อเริ่มต้นการทำงานของ Engine")
