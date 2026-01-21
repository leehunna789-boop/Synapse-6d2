import streamlit as st
import librosa
import numpy as np
import io
import requests
import soundfile as sf
from pydub import AudioSegment

RAW_URL = "https://raw.githubusercontent.com/leehunna789-boop/Synapse-6d2/main/"
FILES = ["vocal.wav", "guitar.wav", "drums.wav", "bass.wav", "others.wav"]

st.title("🛡️ ระบบเปลี่ยนเสียงพูดเป็นเพลง (Full Mix)")

@st.cache_data
def load_all_stems():
    stems = {}
    for f in FILES:
        try:
            r = requests.get(RAW_URL + f, timeout=10)
            if r.status_code == 200:
                # โหลดเป็น numpy สำหรับประมวลผล และ AudioSegment สำหรับรวมเสียง
                y, sr = sf.read(io.BytesIO(r.content))
                stems[f] = {"data": (y if len(y.shape) == 1 else y[:, 0]), "sr": sr, "raw": r.content}
        except: pass
    return stems

all_stems = load_all_stems()

user_voice = st.audio_input("บันทึกเสียงพูดของคุณเพื่อสร้างเพลง")

if user_voice and "vocal.wav" in all_stems:
    with st.spinner("กำลังเปลี่ยนเสียงพูดเป็นเพลงและผสมเสียง..."):
        try:
            # 1. โหลดดนตรีต้นแบบ (Carrier)
            carrier = all_stems["vocal.wav"]["data"]
            sr = all_stems["vocal.wav"]["sr"]
            
            # 2. อ่านเสียงพูด (Modulator)
            y_user, _ = sf.read(io.BytesIO(user_voice.read()))
            if len(y_user.shape) > 1: y_user = y_user[:, 0]
            
            # ปรับความยาวให้เท่ากัน
            y_user = librosa.util.fix_length(y_user, size=len(carrier))
            
            # 3. กระบวนการ Vocoder (สร้างเสียงร้องตามคีย์)
            envelope = np.abs(librosa.hilbert(y_user))
            vocoded_y = librosa.util.normalize(carrier * envelope)
            
            # 4. รวมเสียง (Mix) กับไฟล์อื่นๆ (Guitar, Drums, Bass)
            # แปลงเสียงร้องที่สร้างใหม่เป็น AudioSegment
            out_mem = io.BytesIO()
            sf.write(out_mem, vocoded_y, sr, format='WAV')
            out_mem.seek(0)
            final_vocal = AudioSegment.from_file(out_mem, format="wav")
            
            # เอาไฟล์อื่นมา Overlay
            combined = final_vocal
            for f in ["guitar.wav", "drums.wav", "bass.wav", "others.wav"]:
                if f in all_stems:
                    track = AudioSegment.from_file(io.BytesIO(all_stems[f]["raw"]), format="wav")
                    combined = combined.overlay(track)
            
            # 5. เล่นเพลงที่เสร็จสมบูรณ์
            final_buf = io.BytesIO()
            combined.export(final_buf, format="wav")
            st.audio(final_buf)
            st.success("เพลงของคุณสร้างเสร็จแล้ว! เสียงพูดตรงคีย์คอร์ดทั้งหมดครับ")
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
