import numpy as np
import streamlit as st
from scipy.io import wavfile
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 1. INPUT MODULE
# -----------------------------------------------------------
class InputModule:
    def จัด_โครงสร้าง_คำสั่ง(self, คำสั่งคอร์ด, valence, arousal):
        num_chords = len([c for c in คำสั่งคอร์ด.split(',') if c.strip()])
        total_length = num_chords * 50 if num_chords > 0 else 200
        # สร้าง Sequence จำลอง [Chord, Valence, Arousal]
        symbolic_sequence = np.zeros((total_length, 3))
        symbolic_sequence[:, 1] = valence
        symbolic_sequence[:, 2] = arousal
        return symbolic_sequence

# -----------------------------------------------------------
# 2. AI SYNTHESIS ENGINE (Generating Audio Logic)
# -----------------------------------------------------------
class AISynthesisEngine:
    def __init__(self, samplerate=44100):
        self.sampling_rate = samplerate

    def สังเคราะห์_เสียงสุ่ม_RBF(self, symbolic_sequence):
        valence = symbolic_sequence[0, 1]
        arousal = symbolic_sequence[0, 2]
        
        # กำหนดความยาว 3 วินาที
        duration = 3.0
        num_samples = int(self.sampling_rate * duration)
        
        # --- ลอจิกการสร้างเสียงสุ่มตามอารมณ์ ---
        # Arousal: ควบคุมความแรง (Amplitude)
        noise_amplitude = 0.1 + (arousal * 0.7)
        
        # Valence: ควบคุม "สีสัน" ของเสียงสุ่ม (ใช้การกรองความถี่ต่ำ/สูงจำลอง)
        raw_noise = np.random.uniform(-1, 1, num_samples)
        
        if valence < 0.5:
            # อารมณ์ลบ: เสียงทึบ (Low-pass effect ง่ายๆ โดยการเกลี่ยค่า)
            raw_noise = np.convolve(raw_noise, np.ones(5)/5, mode='same')
        
        audio_out = raw_noise * noise_amplitude
        return audio_out

# -----------------------------------------------------------
# 3. MASTERING MODULE
# -----------------------------------------------------------
class MasteringModule:
    def ใช้_Limiter(self, audio, ceiling=0.9):
        return np.clip(audio, -ceiling, ceiling)

    def process(self, audio_raw, samplerate=44100):
        audio_limited = self.ใช้_Limiter(audio_raw)
        # แปลงเป็น 16-bit PCM
        audio_int16 = (audio_limited * 32767).astype(np.int16)
        return audio_int16

# -----------------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------------
st.set_page_config(page_title="RBF AI Random Sound", layout="wide")
st.title("🎵 RBF AI: Music Synthesis (Random Noise Edition)")

# Sidebar logs
st.sidebar.title("🛠️ Engine Status")

# Layout
col_ctrl, col_viz = st.columns([1, 2])

with col_ctrl:
    st.header("Control Panel")
    chords = st.text_input("Chord Sequence", "C, G, Am, F")
    v = st.slider("Valence (ความสุข)", 0.0, 1.0, 0.5)
    a = st.slider("Arousal (พลังงาน)", 0.0, 1.0, 0.5)
    
    run_btn = st.button("🚀 Start Synthesis", type="primary")

if run_btn:
    # เริ่มกระบวนการ
    input_mod = InputModule()
    engine = AISynthesisEngine()
    master = MasteringModule()

    with st.spinner("กำลังสังเคราะห์เสียง..."):
        # 1. Input
        seq = input_mod.จัด_โครงสร้าง_คำสั่ง(chords, v, a)
        st.sidebar.success("Input Module: Ready")
        
        # 2. Synthesis
        raw_audio = engine.สังเคราะห์_เสียงสุ่ม_RBF(seq)
        st.sidebar.success("AI Engine: Generated")
        
        # 3. Mastering
        final_audio = master.process(raw_audio)
        st.sidebar.success("Mastering: Complete")

    with col_viz:
        st.header("Analysis & Output")
        
        # แสดงกราฟ Waveform
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(raw_audio[:1000], color='#1DB954') # แสดงแค่ 1000 sample แรกเพื่อให้เห็นชัด
        ax.set_title("Waveform (Zoomed)")
        ax.set_ylim(-1, 1)
        st.pyplot(fig)
        
        # เล่นเสียง
        audio_float = final_audio.astype(np.float32) / 32767.0
        st.audio(audio_float, format='audio/wav', sample_rate=44100)
        
        st.info(f"ระดับความแรงของเสียง (Amplitude): {np.max(np.abs(audio_float)):.2f}")

else:
    with col_viz:
        st.info("กรุณากดปุ่มเพื่อเริ่มสังเคราะห์เสียงสุ่ม")
