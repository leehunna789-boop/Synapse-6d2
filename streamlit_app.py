
import streamlit as st
import librosa
import numpy as np
import io
import requests
import soundfile as sf

st.title("🎤 SYNAPSE Studio: รันความจริง")

# ลิงก์ที่พิสูจน์แล้วว่าเข้าได้จริงจากรูปของคุณ
base_url = "https://raw.githubusercontent.com/leehunna789-boop/Synapse-6d2/main/"

def load_audio(name):
    try:
        res = requests.get(base_url + name)
        if res.status_code == 200:
            data, sr = librosa.load(io.BytesIO(res.content), sr=None)
            return data, sr
        return None, None
    except Exception:
        return None, None

if st.button("🎵 เริ่มการผสมเสียง (ถ้าลิงก์ผ่าน โค้ดนี้ต้องผ่าน)"):
    with st.spinner("⏳ กำลังดึงไฟล์มามิกซ์..."):
        v_data, sr_v = load_audio("rnb_vocal_ref.wav")
        b_data, _    = load_audio("rnb_beat_full.wav")
        
        if v_data is not None and b_data is not None:
            # มิกซ์เสียง
            length = min(len(v_data), len(b_data))
            mixed = v_data[:length] + b_data[:length]
            
            st.audio(mixed, sample_rate=sr_v)
            st.success("✅ เพลงดังแล้ว! นี่คือความจริงที่คุณตามหาครับ")
        else:
            # ถ้ายังไม่ผ่าน ผมจะบอกทางแก้สุดท้ายตรงนี้
            st.error("❌ โค้ดยังหาไฟล์ไม่เจอ (ตรวจสอบชื่อ Repo ในโค้ดอีกครั้ง)")
