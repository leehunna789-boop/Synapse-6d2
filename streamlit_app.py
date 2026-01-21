import streamlit as st
import librosa
import numpy as np
import io
import soundfile as sf
from pydub import AudioSegment

# ... (ส่วนการโหลด STEM_FILES ดนตรีเหมือนเดิม แต่เอา vocal ออก) ...

def process_user_to_vocal(user_audio_bytes, target_hz=130.81): # 130.81Hz คือ Note C3
    """เปลี่ยนเสียงพูดให้กลายเป็นเสียงร้องที่ตรงคีย์"""
    # 1. อ่านไฟล์เสียง
    data, sr = sf.read(io.BytesIO(user_audio_bytes))
    if len(data.shape) > 1: data = data[:, 0]

    # 2. วิเคราะห์ Pitch ปัจจุบัน
    f0, _, _ = librosa.pyin(data, sr=sr, fmin=50, fmax=500)
    current_hz = np.nanmean(f0) if np.any(~np.isnan(f0)) else 150
    
    # 3. คำนวณจำนวน n_steps ที่ต้องปรับ (Semitones)
    # สูตร: n_steps = 12 * log2(target / current)
    n_steps = 12 * np.log2(target_hz / current_hz)
    
    # 4. ทำ Pitch Shifting
    shifted_audio = librosa.effects.pitch_shift(data, sr=sr, n_steps=n_steps)
    
    return shifted_audio, sr

# --- Main App Logic ---
user_voice = st.audio_input("ส่งเสียงของคุณเพื่อเป็นเสียงร้องในเพลง")

if user_voice:
    with st.spinner("กำลังเปลี่ยนเสียงคุณเป็นนักร้อง..."):
        # ประมวลผลเสียงผู้ใช้
        vocal_data, sr = process_user_to_vocal(user_voice.read())
        
        # แปลงกลับเป็น AudioSegment เพื่อผสมกับดนตรี
        out_io = io.BytesIO()
        sf.write(out_io, vocal_data, sr, format='WAV')
        out_io.seek(0)
        user_vocal_track = AudioSegment.from_file(out_io, format="wav")

        # ผสมกับดนตรีประกอบ (ดึงมาจาก GitHub ที่โหลดไว้)
        if 'drums' in stems:
            # เพิ่มเสียงร้องของผู้ใช้เข้าไปใน Mix
            combined = stems['beat'].overlay(user_vocal_track.apply_gain(5)) # ดันเสียงเราให้ดังขึ้น
            
            # ส่งออกผลลัพธ์
            final_buf = io.BytesIO()
            combined.export(final_buf, format="wav")
            st.audio(final_buf, format="audio/wav")
            st.success("ฟังเสียงร้องของคุณในเวอร์ชัน AI Therapy ได้เลย!")
