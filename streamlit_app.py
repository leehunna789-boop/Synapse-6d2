import streamlit as st
import time
import random
import numpy as np
import pandas as pd
import io
from scipy.io.wavfile import write
from gtts import gTTS

# ---------------------------------------------------------
# ตั้งค่าหน้าจอ (Theme: Deep Matrix)
# ---------------------------------------------------------
st.set_page_config(page_title="SYNAPSE 6D: DUAL CORE", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* พื้นหลังดำ ตัวหนังสือเขียวเข้มแบบ Hacker */
    .stApp { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    
    /* กรอบแสดงผลข้อมูล */
    .monitor-box {
        border: 1px solid #00FF41;
        padding: 15px;
        background-color: #001100;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    
    /* ตัวหนังสือหัวข้อใหญ่ */
    .big-title { 
        font-size: 45px; 
        font-weight: 900; 
        color: #00FF41; 
        text-align: center; 
        text-shadow: 0 0 15px #00FF41;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ระบบสร้างเสียง (Sound Engine)
# ---------------------------------------------------------
def generate_frequency(freq, duration=5):
    """สร้างเสียงคลื่นความถี่ (Sine Wave)"""
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), False)
    # ผสมคลื่น 2 ลูกให้เสียงดูมีมิติ (Binaural Beats Simulation)
    tone = np.sin(freq * t * 2 * np.pi) + (0.5 * np.sin((freq+4) * t * 2 * np.pi))
    audio = (tone * 0.3 * 32767).astype(np.int16)
    virtual_file = io.BytesIO()
    write(virtual_file, fs, audio)
    return virtual_file

def generate_voice_ai(text):
    """สร้างเสียงพูด AI"""
    try:
        tts = gTTS(text=text, lang='th')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except:
        return None

# ---------------------------------------------------------
# ส่วนแสดงผลหลัก (Main Interface)
# ---------------------------------------------------------
st.markdown('<p class="big-title">SYNAPSE 6D PRO</p>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">SYSTEM STATUS: <span style="color: #00FF41;">ONLINE</span> | DUAL CORE ENGINE</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 INPUT DATA")
    user_input = st.text_area("ป้อนข้อมูลความรู้สึก / Input Text:", height=100)
    
    # ปุ่มกดที่ดูทรงพลัง
    if st.button("🚀 EXECUTE SYNTHESIS (ประมวลผล)", use_container_width=True):
        if user_input:
            # --- ส่วนประมวลผล (Processing) ---
            with st.spinner("Decoding Phonemes & F0 Pitch..."):
                time.sleep(1.5) # เท่ๆ
                
                # คำนวณค่าต่างๆ (Fake Logic ให้ดูเหมือนรูปที่ส่งมา)
                f0_val = random.randint(200, 400)
                phoneme_count = len(user_input) * 2
                freq_hz = 432 + (len(user_input) % 50)
                
                # 1. สร้างเสียงคลื่น (Frequency)
                tone_file = generate_frequency(freq_hz)
                
                # 2. สร้างเสียงพูด (Voice)
                reply_text = f"รับทราบ ระบบได้ปรับจูนความถี่ {freq_hz} เฮิรตซ์ เพื่อความสมดุลของคุณแล้ว"
                voice_file = generate_voice_ai(reply_text)
                
                st.success("SYNTHESIS COMPLETE.")
                
                # --- แสดงผลลัพธ์เสียง (Audio Output) ---
                st.markdown("### 🔊 AUDIO OUTPUT CHANNELS")
                
                st.write(f"**Channel 1: Healing Frequency ({freq_hz} Hz)**")
                st.audio(tone_file, format='audio/wav')
                
                st.write("**Channel 2: AI Voice Guidance**")
                if voice_file:
                    st.audio(voice_file, format='audio/mp3')
                
                # --- ส่วนแสดง Code แบบในรูป (Simulation) ---
                st.markdown("### 🧬 GENERATED SYNTAX (LOG)")
                st.code(f"""
# SYNTHESIS REPORT ID: {random.randint(1000,9999)}
pyworld-tex {{
    input_text = "{user_input[:10]}..."
    phonemes = {{
        count = {phoneme_count}
        base_f0 = {f0_val} Hz
        modulation = 'sine_wave'
    }}
    spectral_envelope {{
        bandwidth = {freq_hz} Hz
        density = 'high_resonance'
    }}
    output_status = 'RENDERED_SUCCESSFULLY'
}}
                """, language="javascript")

with col2:
    st.header("📊 SPECTRAL MONITOR")
    # แสดงกราฟแบบ Real-time (จำลอง)
    
    # กราฟ 1: Pitch Contour
    st.write("📈 F0 Pitch Contour")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['F0', 'Harmonics', 'Noise']
    )
    st.line_chart(chart_data)
    
    # กราฟ 2: Energy Matrix
    st.write("💠 Energy Distribution")
    bar_data = pd.DataFrame({
        'Band': ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
        'Power': np.random.randint(20, 100, 5)
    })
    st.bar_chart(bar_data.set_index('Band'))
    
    # กล่องข้อความเท่ๆ
    st.markdown(f"""
    <div class="monitor-box">
    <b>CORE LOGIC:</b><br>
    > Initializing Vowel Synthesis... OK<br>
    > Loading Acoustic Model... OK<br>
    > Matching Pitch Target... {random.randint(90,100)}%<br>
    > <b>READY TO STREAM</b>
    </div>
    """, unsafe_allow_html=True)

