import numpy as np
import streamlit as st
from scipy.io import wavfile
import io

# ===========================================================
# RBF AI MUSIC SYNTHESIZER (AUTO-GENRE EDITION)
# ===========================================================

class RBAISystem:
    def __init__(self):
        self.fs = 44100
        self.FREQ_MAP = {
            "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63, 
            "F": 349.23, "F#": 369.99, "G": 392.00, "G#": 415.30, "A": 440.00, 
            "A#": 466.16, "B": 493.88
        }
        # ชุดคอร์ดอัตโนมัติแยกตามแนวเพลง
        self.GENRE_PRESETS = {
            "Rap / Hip-Hop": {
                "chords": "Am, F, E, Am", 
                "default_valence": 0.3, 
                "default_arousal": 0.8,
                "desc": "เน้นลูปที่ดุดัน สั้นกระชับ และกดดันเล็กน้อย"
            },
            "R&B / Soul": {
                "chords": "Cmaj7, Am7, Dm7, G7", 
                "default_valence": 0.8, 
                "default_arousal": 0.3,
                "desc": "เน้นความนุ่มนวล โน้ตลากยาว และเสียงที่พริ้วไหว"
            }
        }

    def generate_audio(self, chords_str, valence, arousal):
        chords = [c.strip() for c in chords_str.split(',') if c.strip()]
        final_audio = np.array([], dtype=np.float32)

        for chord_name in chords:
            # ดึงเฉพาะตัวอักษรแรกเพื่อหาความถี่ (Simple Root Note)
            root = chord_name[0].upper()
            if len(chord_name) > 1 and chord_name[1] == '#':
                root += '#'
            
            freq = self.FREQ_MAP.get(root, 261.63)
            
            # RBF Logic:
            duration = 1.5 - (arousal * 1.0) # Arousal สูง = โน้ตสั้นลง
            t = np.linspace(0, duration, int(self.fs * duration), endpoint=False)
            
            # Timbre: R&B จะนุ่มกว่า (Sine), Rap จะแข็งกว่า (Saw)
            wave = (valence * np.sin(2 * np.pi * freq * t)) + \
                   ((1 - valence) * (2 * (t * freq - np.floor(0.5 + t * freq))))
            
            # Amplitude: Arousal สูง = เสียงดังและกระแทก
            amp = 0.2 + (arousal * 0.5)
            
            # ADSR Envelope
            fade = int(self.fs * 0.05)
            envelope = np.ones_like(wave)
            envelope[:fade] = np.linspace(0, 1, fade)
            envelope[-fade:] = np.linspace(1, 0, fade)
            
            final_audio = np.concatenate([final_audio, wave * amp * envelope])
            
        return np.clip(final_audio, -0.9, 0.9)

# --- UI SECTION ---
st.set_page_config(layout="wide", page_title="RBF Auto-Genre")
st.title("🎼 RBF AI: Auto-Genre Synthesizer")

system = RBAISystem()

# Sidebar แสดงสถานะ API (ถ้ามี)
if "GEMINI_API_KEY" in st.secrets:
    st.sidebar.success("✅ API Key: Standby")
else:
    st.sidebar.warning("⚠️ Local Mode Active")
st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")

# ส่วนเลือกแนวเพลง
st.subheader("1. เลือกแนวเพลงที่ต้องการ")
genre = st.radio("แนวเพลง (Genre):", list(system.GENRE_PRESETS.keys()), horizontal=True)

# ดึงค่าจาก Preset
preset = system.GENRE_PRESETS[genre]

# แสดงค่าที่เลือกอัตโนมัติ (แต่ยังยอมให้ผู้ใช้ปรับแต่งเองได้)
col1, col2, col3 = st.columns(3)
with col1:
    chord_input = st.text_input("ชุดคอร์ด (ปรับแต่งได้):", preset["chords"])
with col2:
    v = st.slider("Valence (ความนุ่มนวล)", 0.0, 1.0, preset["default_valence"])
with col3:
    a = st.slider("Arousal (พลังงาน/ความเร็ว)", 0.0, 1.0, preset["default_arousal"])

st.caption(f"💡 **สไตล์ของ {genre}:** {preset['desc']}")

if st.button("🚀 เริ่มสังเคราะห์เพลงอัตโนมัติ", type="primary"):
    with st.spinner(f"กำลังสร้างเสียงสไตล์ {genre}..."):
        audio_data = system.generate_audio(chord_input, v, a)
        
        st.success(f"เสร็จสมบูรณ์! นี่คือเสียงแนว {genre}")
        
        # Visualizer
        st.line_chart(audio_data[:4000])
        
        # Playback
        st.audio(audio_data, sample_rate=44100)
        
        # Download
        buffer = io.BytesIO()
        wavfile.write(buffer, 44100, (audio_data * 32767).astype(np.int16))
        st.download_button("⬇️ ดาวน์โหลด WAV", buffer.getvalue(), f"{genre}_rbf.wav")
