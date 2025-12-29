import streamlit as st
import numpy as np
import scipy.io.wavfile as wavfile
import os

# --- 1. SET THEME & LAYOUT (ตามสไตล์ SYNAPSE) ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'Kanit', sans-serif; }
    .neon-red-logo { color: #FF0000; text-shadow: 0 0 25px #FF0000; font-size: 65px; text-align: center; font-weight: 900; }
    .luxury-card {
        background: rgba(20, 20, 20, 0.9);
        border: 2px solid #00F2FE;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0px 8px 25px rgba(0, 242, 254, 0.3);
    }
    h1, h2, h3, p { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="neon-red-logo">SYNAPSE</p>', unsafe_allow_html=True)

# --- 2. ฟังก์ชันผสมเสียงจริง (The Mixer) ---
def mix_real_audio():
    vocal_file = "my_vocal.wav"
    bass_file = "rap_bass.wav"
    
    # ตรวจสอบว่าไฟล์มีอยู่จริงไหม (เพื่อป้องกัน Error เสียงเงียบ)
    if not os.path.exists(vocal_file) or not os.path.exists(bass_file):
        st.error(f"❌ ระบบหาไฟล์เสียงไม่เจอ! กรุณาเช็กชื่อไฟล์บน GitHub (ต้องเป็น {vocal_file} และ {bass_file})")
        return None, None

    # โหลดไฟล์เสียงจริง
    sr_v, vocal = wavfile.read(vocal_file)
    sr_b, bass = wavfile.read(bass_file)

    # แปลงเป็น Float เพื่อป้องกันเสียงแตกขณะผสม
    vocal = vocal.astype(np.float32)
    bass = bass.astype(np.float32)

    # ทำให้ความยาวเท่ากัน
    min_len = min(len(vocal), len(bass))
    vocal = vocal[:min_len]
    bass = bass[:min_len]

    # ผสมเสียง (1.0 คือเสียงเต็ม / 0.8 คือลดเสียงดนตรีลงนิดนึงเพื่อให้เสียงร้องชัด)
    combined = (vocal * 1.0) + (bass * 0.8)

    # Normalize เสียงเพื่อให้ดังชัดเจนและไม่แตก
    combined = combined / np.max(np.abs(combined))
    
    # แปลงกลับเป็น Int16 เพื่อให้ Streamlit เล่นได้
    final_audio = (combined * 32767).astype(np.int16)
    
    return final_audio, sr_v

# --- 3. DASHBOARD UI ---
st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
st.subheader("🎼 ระบบรวมเสียงร้องและดนตรีจริง")
st.write("สถานะไฟล์: `my_vocal.wav` และ `rap_bass.wav` พร้อมทำงาน")

if st.button("🚀 ACTIVATE SYNAPSE 6D", type="primary"):
    with st.spinner("กำลังดึงเสียงจริงจาก GitHub มาผสม..."):
        audio_out, sr = mix_real_audio()
        
        if audio_out is not None:
            st.success("✅ รวมเสียงสำเร็จ! กดฟังได้ที่ด้านล่างนี้")
            # แสดง Waveform ให้เห็นว่ามีเสียงจริงๆ
            st.line_chart(audio_out[:5000]) 
            # ตัวเล่นเสียง
            st.audio(audio_out, sample_rate=sr)
st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")
