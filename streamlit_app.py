import streamlit as st
import librosa
import numpy as np
import io
import requests
from pydub import AudioSegment
import soundfile as sf

# 1. ตั้งค่า URL ให้ชัวร์ (ตรวจสอบว่าตัวสะกดพิมพ์เล็ก-ใหญ่ตรงกับใน GitHub)
RAW_URL = "https://raw.githubusercontent.com/leehunna789-boop/Synapse-6d2/main/"
STEM_FILES = {
    "vocal": "rnb_vocal_ref.wav",
    "guitar": "rnb_guitar.wav",
    "bass": "rnb_bass.wav",
    "drums": "rnb_drums.wav",
    "beat": "rnb_beat_full.wav"
}

st.set_page_config(page_title="Synapse AI Therapy", page_icon="🛡️")
st.title("🛡️ ระบบบำบัดด้วยเสียง (Synapse-6d2)")

# ฟังก์ชันดึงไฟล์ที่ออกแบบมาให้ 'ไม่พัง' แม้เน็ตหลุด
@st.cache_data(show_spinner=False)
def load_audio_github(file_name):
    url = RAW_URL + file_name
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            return AudioSegment.from_file(io.BytesIO(r.content), format="wav")
    except Exception as e:
        st.error(f"โหลดไฟล์ {file_name} ไม่ได้: {e}")
    return None

# --- ส่วนรับเสียงผู้ใช้ ---
user_voice = st.audio_input("แตะเพื่อพูด (ระบบจะวิเคราะห์ความถี่เสียงของคุณ)")

if user_voice:
    with st.spinner("กำลังประมวลผล Logic บำบัด..."):
        try:
            # ใช้ soundfile อ่านแทนเพื่อความเสถียรบน Streamlit
            data, samplerate = sf.read(io.BytesIO(user_voice.read()))
            
            # วัดค่า Hz (ถ้าเป็น Stereo เอาแค่ Mono มาคำนวณ)
            if len(data.shape) > 1: data = data[:, 0]
            
            f0, _, _ = librosa.pyin(data, sr=samplerate, fmin=50, fmax=500)
            avg_hz = np.nanmean(f0) if np.any(~np.isnan(f0)) else 150
            
            st.metric("ความถี่เสียงที่วัดได้", f"{avg_hz:.2f} Hz")

            # --- โหลดและผสมเสียง ---
            stems = {}
            for key, name in STEM_FILES.items():
                track = load_audio_github(name)
                if track:
                    stems[key] = track

            if len(stems) >= 5:
                # Logic มาตรฐาน: ถ้าเสียงทุ้ม (Hz < 130) = ต้องการการปลอบโยน
                v_vol, d_vol, b_vol = 0, 0, 0
                if avg_hz < 130:
                    st.info("💡 โหมดปลอบประโลม: ลดความแรงของจังหวะลง")
                    v_vol = 3    # ดันเสียงร้อง
                    d_vol = -12  # ลดกลอง
                    b_vol = -5   # ลดเบส
                
                # ผสมเสียง (Mixing)
                combined = stems['vocal'].apply_gain(v_vol).overlay(
                           stems['guitar']).overlay(
                           stems['bass'].apply_gain(b_vol)).overlay(
                           stems['drums'].apply_gain(d_vol)).overlay(
                           stems['beat'].apply_gain(d_vol))
                
                # ส่งออกผลลัพธ์
                out_buf = io.BytesIO()
                combined.export(out_buf, format="wav")
                st.audio(out_buf, format="audio/wav")
                st.success("เรียบร้อย! เพลงถูกปรับจูนตามระดับเสียงของคุณแล้ว")
            else:
                st.error("ดึงไฟล์จาก GitHub ไม่ครบ ตรวจสอบชื่อไฟล์อีกครั้งครับ")
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในระบบวิเคราะห์: {e}")
