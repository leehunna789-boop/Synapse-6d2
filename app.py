import streamlit as st
import numpy as np
import scipy.io.wavfile as wavfile
import os

# --- 1. SET THEME & LAYOUT ---
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

# --- 2. ฟังก์ชันผสมเสียงเวอร์ชันแก้ ValueError ---
def mix_real_audio():
    vocal_file = "my_vocal.wav"
    bass_file = "rap_bass.wav"
    
    if not os.path.exists(vocal_file) or not os.path.exists(bass_file):
        st.error("❌ หาไฟล์ไม่เจอ กรุณาตรวจสอบชื่อไฟล์บน GitHub")
        return None, None

    # โหลดไฟล์
    sr_v, vocal = wavfile.read(vocal_file)
    sr_b, bass = wavfile.read(bass_file)

    # ฟังก์ชันจัดการให้เป็น Mono (แก้ปัญหา Stereo บวกกับ Mono ไม่ได้)
    def to_mono(data):
        if len(data.shape) > 1:
            return data.mean(axis=1)
        return data

    vocal = to_mono(vocal.astype(np.float32))
    bass = to_mono(bass.astype(np.float32))

    # ทำให้ความยาวเท่ากันเป๊ะๆ (แก้ ValueError: operands could not be broadcast together)
    min_len = min(len(vocal), len(bass))
    vocal = vocal[:min_len]
    bass = bass[:min_len]

    # ผสมเสียง
    combined = (vocal * 1.0) + (bass * 0.8)

    # Normalize ป้องกันเสียงแตก
    max_val = np.max(np.abs(combined))
    if max_val > 0:
        combined = combined / max_val
    
    final_audio = (combined * 32767).astype(np.int16)
    return final_audio, sr_v

# --- 3. UI ---
st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
st.subheader("🎼 ระบบรวมเสียงร้องและดนตรีจริง")

if st.button("🚀 ACTIVATE SYNAPSE 6D", type="primary"):
    with st.spinner("กำลังแก้ปัญหาและผสมเสียง..."):
        try:
            audio_out, sr = mix_real_audio()
            if audio_out is not None:
                st.success("✅ ผสมเสียงสำเร็จ!")
                st.audio(audio_out, sample_rate=sr)
                st.line_chart(audio_out[:5000])
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
st.markdown('</div>', unsafe_allow_html=True)
