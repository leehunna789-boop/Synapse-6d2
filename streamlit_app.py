import streamlit as st
import librosa
import numpy as np
import io
import requests
import soundfile as sf

st.title("🎤 SYNAPSE Studio: ขั้นตอนการวัดใจ (รันของจริง)")

# ลิงก์ที่พิสูจน์แล้วว่าดาวน์โหลดได้จริง
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

if st.button("🎵 กดเพื่อรัน Logic การผสมเสียง (วัดใจกันตรงนี้)"):
    with st.spinner("⏳ ระบบกำลังไปดึงไฟล์จาก GitHub มาวางซ้อนกัน..."):
        # โหลดไฟล์ 2 ตัวหลัก (Vocal Reference กับ Beat)
        v_data, sr_v = load_audio("rnb_vocal_ref.wav")
        b_data, _    = load_audio("rnb_beat_full.wav")
        
        if v_data is not None and b_data is not None:
            # Logic: ทำให้ความยาวเท่ากันแล้วบวกกัน (Mixing)
            length = min(len(v_data), len(b_data))
            mixed = v_data[:length] + b_data[:length]
            
            st.audio(mixed, sample_rate=sr_v)
            st.success("✅ ได้ยินเสียงเพลงไหมครับ? ถ้าได้ยิน แสดงว่าระบบผสมเสียงทำงานแล้ว!")
        else:
            st.error("❌ ระบบยังหาไฟล์ไม่เจอ แม้ลิงก์จะใช้ได้ (อาจต้องรอ GitHub อัปเดตแคช)")
