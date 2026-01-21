import streamlit as st
import librosa
import numpy as np
import io
import requests
from pydub import AudioSegment

# ฟังก์ชันโหลดเสียงที่ "กันตาย" (ถ้าโหลดไม่ได้ให้แจ้งเตือน)
def fetch_audio(url):
    try:
        req = requests.get(url, timeout=10)
        if req.status_code == 200:
            return AudioSegment.from_file(io.BytesIO(req.content), format="wav")
        else:
            st.error(f"โหลดไฟล์ไม่สำเร็จ: {url.split('/')[-1]}") return None
    except: return None

st.title("🛡️ ระบบบำบัดด้วยเสียง (ฉบับใช้งานจริง)")

# --- ตั้งค่า URL ของคุณ ---
# ตัวอย่าง: https://raw.githubusercontent.com/ชื่อคุณ/โปรเจกต์/main/
BASE_URL = "ใส่ลิงก์ RAW ของคุณที่นี่/" 
FILES = ["vocal.wav", "guitar.wav", "bass.wav", "drums.wav", "others.wav"]

# ส่วนรับเสียงพูดผู้ใช้
user_voice = st.audio_input("กดเพื่อพูดประโยคสั้นๆ")

if user_voice:
    with st.spinner("ระบบกำลังทำงาน..."):
        # 1. วิเคราะห์ Hz
        y, sr = librosa.load(user_voice)
        f0, _, _ = librosa.pyin(y, fmin=50, fmax=500)
        hz = np.nanmean(f0) if np.any(~np.isnan(f0)) else 150
        
        st.write(f"วัดความถี่ได้: {hz:.2f} Hz")

        # 2. โหลดและมิกซ์ (Logic ตามที่ตกลงกัน)
        tracks = []
        for f in FILES:
            track = fetch_audio(BASE_URL + f)
            if track: tracks.append(track)
        
        if len(tracks) == 5:
            # มิกซ์เสียงตาม Hz (ตัวอย่าง: ถ้าเศร้า ลดกลอง)
            vocal, guitar, bass, drums, others = tracks
            if hz < 130:
                drums = drums - 15 # ลดกลอง 15 เดซิเบล
                st.info("โหมด: ปลอบประโลม")
            
            # รวมร่าง
            final = vocal.overlay(guitar).overlay(bass).overlay(drums).overlay(others)
            
            # ส่งผลลัพธ์
            out = io.BytesIO()
            final.export(out, format="wav")
            st.audio(out)
        else:
            st.warning("ไฟล์ Stems ใน GitHub ไม่ครบ 5 ไฟล์ครับ")
