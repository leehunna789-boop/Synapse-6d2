import streamlit as st
import librosa
import numpy as np
import io
import requests
from pydub import AudioSegment
import soundfile as sf

# 1. ตั้งค่าไฟล์ตัวอย่าง (Sample) จาก GitHub
RAW_URL = "https://raw.githubusercontent.com/leehunna789-boop/Synapse-6d2/main/"
# ใช้ไฟล์ vocal.wav หรือ rnb_vocal_ref.wav เป็นต้นแบบของระดับเสียง
SAMPLE_VOCAL = "vocal.wav" 

st.title("🛡️ ระบบปรับเสียงพูดให้ตรงกับเสียงตัวอย่าง")

# --- โหลดไฟล์ตัวอย่างเพื่อหา Pitch ต้นแบบ ---
@st.cache_data
def get_sample_pitch():
    try:
        r = requests.get(RAW_URL + SAMPLE_VOCAL, timeout=15)
        if r.status_code == 200:
            data, sr = sf.read(io.BytesIO(r.content))
            if len(data.shape) > 1: data = data[:, 0]
            # หาความถี่เฉลี่ยของเสียงต้นแบบ
            f0, _, _ = librosa.pyin(data, sr=sr, fmin=50, fmax=500)
            return np.nanmean(f0)
    except:
        return 130.81 # ค่าเริ่มต้นถ้าโหลดไม่ได้ (Note C)
    return 130.81

target_pitch = get_sample_pitch()

# 2. ส่วนรับเสียงของคุณ
user_voice = st.audio_input("ส่งเสียงพูดของคุณ (ระบบจะปรับให้ตรงกับเสียงตัวอย่าง)")

if user_voice:
    with st.spinner("กำลังปรับระดับเสียง..."):
        try:
            # อ่านเสียงที่คุณพูด
            y, sr = sf.read(io.BytesIO(user_voice.read()))
            if len(y.shape) > 1: y = y[:, 0]

            # หาความถี่เสียงที่คุณพูด
            f0_user, _, _ = librosa.pyin(y, sr=sr, fmin=50, fmax=500)
            current_pitch = np.nanmean(f0_user) if np.any(~np.isnan(f0_user)) else 150

            # คำนวณระยะห่างเพื่อปรับ (Pitch Shifting)
            # n_steps คือจำนวนครึ่งเสียงที่ต้องปรับเพื่อให้เท่ากับต้นแบบ
            n_steps = 12 * np.log2(target_pitch / current_pitch)

            # ปรับเสียงพูดของเราให้ตรงกับตัวอย่าง
            shifted_audio = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

            # 3. ส่งผลลัพธ์ออกมา
            out_buf = io.BytesIO()
            sf.write(out_buf, shifted_audio, sr, format='WAV')
            
            st.write(f"ระดับเสียงต้นแบบ: {target_pitch:.2f} Hz | เสียงของคุณ: {current_pitch:.2f} Hz")
            st.audio(out_buf, format="audio/wav")
            st.success("ปรับเสียงให้ตรงกับตัวอย่างเรียบร้อยแล้ว!")

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
